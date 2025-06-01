from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import logging

# AWS SES imports
try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    AWS_SES_AVAILABLE = True
except ImportError:
    AWS_SES_AVAILABLE = False
    logging.warning("boto3 not installed. Falling back to Django's email backend.")

logger = logging.getLogger(__name__)


def send_otp_email_aws_ses(email, otp_code):
    """Send OTP verification email using AWS SES API"""
    
    if not AWS_SES_AVAILABLE:
        logger.warning("AWS SES not available, falling back to Django email backend")
        return send_otp_email(email, otp_code)
    
    # Check for AWS credentials
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None) or os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None) or os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = getattr(settings, 'AWS_SES_REGION', 'us-east-1')
    
    if not aws_access_key or not aws_secret_key:
        logger.warning("AWS credentials not configured, falling back to Django email backend")
        return send_otp_email(email, otp_code)
    
    try:
        # Create SES client
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        from_email = getattr(settings, 'AWS_SES_FROM_EMAIL', 'noreply@scholarshipportal.com')
        
        # HTML content
        html_content = get_otp_html_template(otp_code)
        
        # Plain text content
        plain_content = get_otp_plain_template(otp_code)
        
        # Send email
        response = ses_client.send_email(
            Source=f'Scholarship Portal <{from_email}>',
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': 'Verify your email - Scholarship Portal',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': plain_content,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': html_content,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        logger.info(f"OTP email sent successfully to {email} via AWS SES. MessageId: {response['MessageId']}")
        return True
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS SES ClientError: {error_code} - {error_message}")
        # Fallback to Django email backend
        return send_otp_email(email, otp_code)
    except NoCredentialsError:
        logger.error("AWS credentials not found")
        return send_otp_email(email, otp_code)
    except Exception as e:
        logger.error(f"Failed to send email via AWS SES: {e}")
        # Fallback to Django email backend
        return send_otp_email(email, otp_code)


def get_otp_html_template(otp_code):
    """Get HTML template for OTP email"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification - Scholarship Portal</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f7fafc;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .header p {{
                margin: 10px 0 0;
                opacity: 0.9;
                font-size: 16px;
            }}
            .content {{
                padding: 40px;
            }}
            .content h2 {{
                color: #2d3748;
                margin-top: 0;
                font-size: 24px;
            }}
            .otp-container {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 12px;
                padding: 30px;
                text-align: center;
                margin: 30px 0;
            }}
            .otp-label {{
                color: white;
                font-size: 16px;
                margin-bottom: 15px;
                font-weight: 500;
            }}
            .otp-code {{
                font-size: 36px;
                font-weight: 800;
                color: white;
                letter-spacing: 8px;
                margin: 15px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            .otp-expiry {{
                color: rgba(255,255,255,0.9);
                font-size: 14px;
                margin-top: 15px;
            }}
            .security-note {{
                background-color: #fed7d7;
                border-left: 4px solid #f56565;
                padding: 20px;
                margin: 30px 0;
                border-radius: 6px;
            }}
            .security-note strong {{
                color: #c53030;
            }}
            .footer {{
                background-color: #f7fafc;
                padding: 30px;
                text-align: center;
                color: #718096;
                font-size: 14px;
                border-top: 1px solid #e2e8f0;
            }}
            .logo {{
                font-size: 24px;
                margin-bottom: 10px;
            }}
            @media (max-width: 600px) {{
                .content {{
                    padding: 20px;
                }}
                .otp-code {{
                    font-size: 28px;
                    letter-spacing: 4px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🎓</div>
                <h1>Scholarship Portal</h1>
                <p>Email Verification Required</p>
            </div>
            
            <div class="content">
                <h2>Welcome to Scholarship Portal!</h2>
                <p>Thank you for joining our community! To complete your registration and start exploring amazing scholarship opportunities, please verify your email address.</p>
                
                <div class="otp-container">
                    <div class="otp-label">Your verification code is:</div>
                    <div class="otp-code">{otp_code}</div>
                    <div class="otp-expiry">⏰ This code expires in 10 minutes</div>
                </div>
                
                <p>Enter this 6-digit code on the verification page to activate your account and unlock access to thousands of scholarship opportunities.</p>
                
                <div class="security-note">
                    <strong>🔒 Security Notice:</strong> This is an automated security email. If you didn't request this verification, please ignore this email and do not share this code with anyone.
                </div>
                
                <p>Need help? Contact our support team at support@scholarshipportal.com</p>
            </div>
            
            <div class="footer">
                <p><strong>Scholarship Portal</strong></p>
                <p>Making education accessible for everyone</p>
                <p>© 2025 Scholarship Portal. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_otp_plain_template(otp_code):
    """Get plain text template for OTP email"""
    return f"""
🎓 SCHOLARSHIP PORTAL - Email Verification

Welcome to Scholarship Portal!

Thank you for joining our community! To complete your registration and start exploring scholarship opportunities, please verify your email address.

Your verification code is: {otp_code}

⏰ This code expires in 10 minutes.

Enter this 6-digit code on the verification page to activate your account.

🔒 Security Notice: If you didn't request this verification, please ignore this email and do not share this code with anyone.

Need help? Contact us at support@scholarshipportal.com

Best regards,
Scholarship Portal Team

---
© 2025 Scholarship Portal. All rights reserved.
    """


def send_otp_email(email, otp_code):
    """Send OTP verification email to user (fallback method using Django's email backend)"""
    
    subject = 'Verify your email - Scholarship Portal'
    
    # Create HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Email Verification - Scholarship Portal</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #2563eb;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background-color: #f8fafc;
                padding: 30px;
                border-radius: 0 0 8px 8px;
                border: 1px solid #e2e8f0;
            }}
            .otp-box {{
                background-color: #fff;
                border: 2px solid #2563eb;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                margin: 20px 0;
            }}
            .otp-code {{
                font-size: 32px;
                font-weight: bold;
                color: #2563eb;
                letter-spacing: 8px;
                margin: 10px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #64748b;
                font-size: 14px;
            }}
            .warning {{
                background-color: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 15px;
                margin: 20px 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 Scholarship Portal</h1>
            <p>Email Verification Required</p>
        </div>
        
        <div class="content">
            <h2>Welcome to Scholarship Portal!</h2>
            <p>Thank you for registering with us. To complete your account setup, please verify your email address using the OTP code below:</p>
            
            <div class="otp-box">
                <p>Your verification code is:</p>
                <div class="otp-code">{otp_code}</div>
                <p style="margin: 0; color: #64748b; font-size: 14px;">This code expires in 10 minutes</p>
            </div>
            
            <p>Enter this code on the verification page to activate your account and start exploring scholarship opportunities.</p>
            
            <div class="warning">
                <strong>Security Note:</strong> If you didn't request this verification, please ignore this email. Never share this code with anyone.
            </div>
        </div>
        
        <div class="footer">
            <p>This is an automated message from Scholarship Portal.</p>
            <p>© 2025 Scholarship Portal. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    plain_message = f"""
    Welcome to Scholarship Portal!
    
    Thank you for registering with us. To complete your account setup, please verify your email address.
    
    Your verification code is: {otp_code}
    
    This code expires in 10 minutes. Enter this code on the verification page to activate your account.
    
    If you didn't request this verification, please ignore this email.
    
    Best regards,
    Scholarship Portal Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_verification_email(email, otp_code):
    """
    Main function to send verification email.
    Uses AWS SES by default, falls back to Django email backend if AWS SES fails.
    """
    try:
        # Try AWS SES first
        if send_otp_email_aws_ses(email, otp_code):
            logger.info(f"Verification email sent successfully to {email} via AWS SES")
            return True
        else:
            logger.warning("AWS SES failed, trying Django email backend")
            return send_otp_email(email, otp_code)
    except Exception as e:
        logger.error(f"All email sending methods failed: {e}")
        return False


def send_welcome_email_aws_ses(email, full_name):
    """Send welcome email using AWS SES API"""
    
    if not AWS_SES_AVAILABLE:
        logger.warning("AWS SES not available, falling back to Django email backend")
        return send_welcome_email_django(email, full_name)
    
    # Check for AWS credentials
    aws_access_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None) or os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None) or os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = getattr(settings, 'AWS_SES_REGION', 'us-east-1')
    
    if not aws_access_key or not aws_secret_key:
        logger.warning("AWS credentials not configured, falling back to Django email backend")
        return send_welcome_email_django(email, full_name)
    
    try:
        # Create SES client
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        from_email = getattr(settings, 'AWS_SES_FROM_EMAIL', 'noreply@scholarshipportal.com')
        
        # HTML content
        html_content = get_welcome_html_template(full_name)
        
        # Plain text content
        plain_content = get_welcome_plain_template(full_name)
        
        # Send email
        response = ses_client.send_email(
            Source=f'Scholarship Portal <{from_email}>',
            Destination={
                'ToAddresses': [email],
            },
            Message={
                'Subject': {
                    'Data': 'Welcome to Scholarship Portal!',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': plain_content,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': html_content,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        logger.info(f"Welcome email sent successfully to {email} via AWS SES. MessageId: {response['MessageId']}")
        return True
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS SES ClientError: {error_code} - {error_message}")
        # Fallback to Django email backend
        return send_welcome_email_django(email, full_name)
    except NoCredentialsError:
        logger.error("AWS credentials not found")
        return send_welcome_email_django(email, full_name)
    except Exception as e:
        logger.error(f"Failed to send welcome email via AWS SES: {e}")
        # Fallback to Django email backend
        return send_welcome_email_django(email, full_name)


def get_welcome_html_template(full_name):
    """Get HTML template for welcome email"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Scholarship Portal</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f7fafc;
            }}
            .container {{
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: 700;
            }}
            .content {{
                padding: 40px;
            }}
            .welcome-message {{
                font-size: 18px;
                color: #2d3748;
                margin-bottom: 20px;
            }}
            .feature-list {{
                background-color: #f7fafc;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }}
            .feature-item {{
                display: flex;
                align-items: center;
                margin: 10px 0;
                color: #4a5568;
            }}
            .feature-icon {{
                margin-right: 10px;
                font-size: 16px;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                background-color: #f7fafc;
                padding: 30px;
                text-align: center;
                color: #718096;
                font-size: 14px;
                border-top: 1px solid #e2e8f0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div style="font-size: 36px; margin-bottom: 10px;">🎓</div>
                <h1>Welcome to Scholarship Portal!</h1>
                <p>Your journey to educational excellence begins here</p>
            </div>
            
            <div class="content">
                <div class="welcome-message">
                    <strong>Hi {full_name or 'there'}!</strong>
                </div>
                
                <p>Congratulations! Your account has been successfully created and verified. You're now part of a community dedicated to making education accessible for everyone.</p>
                
                <div class="feature-list">
                    <h3 style="margin-top: 0; color: #2d3748;">What you can do now:</h3>
                    <div class="feature-item">
                        <span class="feature-icon">🔍</span>
                        <span>Search and discover thousands of scholarship opportunities</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">❤️</span>
                        <span>Save scholarships that match your interests</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📝</span>
                        <span>Apply for scholarships directly through our platform</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">👤</span>
                        <span>Complete your profile for personalized recommendations</span>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📊</span>
                        <span>Track your application progress</span>
                    </div>
                </div>
                
                <div style="text-align: center;">
                    <a href="http://localhost:3000/scholarships/search" class="cta-button">
                        🚀 Start Exploring Scholarships
                    </a>
                </div>
                
                <p>If you have any questions or need assistance, our support team is here to help at <a href="mailto:support@scholarshipportal.com">support@scholarshipportal.com</a>.</p>
                
                <p>Best of luck with your scholarship journey!</p>
            </div>
            
            <div class="footer">
                <p><strong>Scholarship Portal</strong></p>
                <p>Making education accessible for everyone</p>
                <p>© 2025 Scholarship Portal. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """


def get_welcome_plain_template(full_name):
    """Get plain text template for welcome email"""
    return f"""
🎓 WELCOME TO SCHOLARSHIP PORTAL!

Hi {full_name or 'there'}!

Congratulations! Your account has been successfully created and verified. You're now part of a community dedicated to making education accessible for everyone.

What you can do now:
🔍 Search and discover thousands of scholarship opportunities
❤️ Save scholarships that match your interests  
📝 Apply for scholarships directly through our platform
👤 Complete your profile for personalized recommendations
📊 Track your application progress

Start exploring scholarships: http://localhost:3000/scholarships/search

If you have any questions or need assistance, our support team is here to help at support@scholarshipportal.com.

Best of luck with your scholarship journey!

Scholarship Portal Team

---
© 2025 Scholarship Portal. All rights reserved.
    """


def send_welcome_email_django(user_or_email, full_name=None):
    """Send welcome email using Django's email backend (fallback method)"""
    
    # Handle both user object and separate email/name parameters
    if hasattr(user_or_email, 'email'):
        # It's a user object
        email = user_or_email.email
        name = getattr(user_or_email, 'full_name', '') or user_or_email.email
    else:
        # It's an email string with separate name
        email = user_or_email
        name = full_name or 'there'
    
    subject = 'Welcome to Scholarship Portal! 🎓'
    
    # Create HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Welcome to Scholarship Portal</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #48bb78;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background-color: #f8fafc;
                padding: 30px;
                border-radius: 0 0 8px 8px;
                border: 1px solid #e2e8f0;
            }}
            .feature-list {{
                background-color: #fff;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }}
            .feature-item {{
                margin: 10px 0;
                color: #4a5568;
            }}
            .cta-button {{
                display: inline-block;
                background-color: #667eea;
                color: white;
                padding: 15px 30px;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #64748b;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 Welcome to Scholarship Portal!</h1>
            <p>Your journey to educational excellence begins here</p>
        </div>
        
        <div class="content">
            <h2>Hi {name}!</h2>
            
            <p>Congratulations! Your account has been successfully created and verified. You're now part of a community dedicated to making education accessible for everyone.</p>
            
            <div class="feature-list">
                <h3>What you can do now:</h3>
                <div class="feature-item">🔍 Search and discover thousands of scholarship opportunities</div>
                <div class="feature-item">❤️ Save scholarships that match your interests</div>
                <div class="feature-item">📝 Apply for scholarships directly through our platform</div>
                <div class="feature-item">👤 Complete your profile for personalized recommendations</div>
                <div class="feature-item">📊 Track your application progress</div>
            </div>
            
            <div style="text-align: center;">
                <a href="http://localhost:3000/scholarships/search" class="cta-button">
                    🚀 Start Exploring Scholarships
                </a>
            </div>
            
            <p>If you have any questions or need assistance, our support team is here to help at <a href="mailto:support@scholarshipportal.com">support@scholarshipportal.com</a>.</p>
            
            <p>Best of luck with your scholarship journey!</p>
        </div>
        
        <div class="footer">
            <p><strong>Scholarship Portal</strong></p>
            <p>Making education accessible for everyone</p>
            <p>© 2025 Scholarship Portal. All rights reserved.</p>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    plain_message = f"""
    Welcome to Scholarship Portal!
    
    Hi {name}!
    
    Congratulations! Your account has been successfully created and verified. You're now part of a community dedicated to making education accessible for everyone.
    
    What you can do now:
    🔍 Search and discover thousands of scholarship opportunities
    ❤️ Save scholarships that match your interests  
    📝 Apply for scholarships directly through our platform
    👤 Complete your profile for personalized recommendations
    📊 Track your application progress
    
    Start exploring scholarships: http://localhost:3000/scholarships/search
    
    If you have any questions or need assistance, our support team is here to help at support@scholarshipportal.com.
    
    Best of luck with your scholarship journey!
    
    Scholarship Portal Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        return False


def send_welcome_email(user):
    """
    Main function to send welcome email.
    Uses AWS SES by default, falls back to Django email backend if AWS SES fails.
    """
    try:
        # Try AWS SES first
        if send_welcome_email_aws_ses(user.email, user.full_name):
            logger.info(f"Welcome email sent successfully to {user.email} via AWS SES")
            return True
        else:
            logger.warning("AWS SES failed for welcome email, trying Django email backend")
            return send_welcome_email_django(user)
    except Exception as e:
        logger.error(f"All welcome email sending methods failed: {e}")
        return False
