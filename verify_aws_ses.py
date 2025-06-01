#!/usr/bin/env python
"""
Simple test script to verify AWS SES credentials and email sending capability.
This script will help diagnose if there are issues with your AWS SES configuration.
"""

import os
import sys
import smtplib
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def color_print(message, color="white"):
    """Print colored text to console"""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "end": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{message}{colors['end']}")


def test_aws_ses_api_credentials():
    """Test AWS SES API credentials"""
    color_print("\n🔑 Testing AWS SES API Credentials...", "blue")
    
    # Get credentials from environment
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_SES_SMTP_USERNAME')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY') or os.environ.get('AWS_SES_SMTP_PASSWORD')
    aws_region = os.environ.get('AWS_SES_REGION', 'eu-north-1')
    
    if not aws_access_key or not aws_secret_key:
        color_print("❌ No AWS credentials found in environment", "red")
        return False

    try:
        # Try to create an SES client
        color_print(f"👉 Creating SES client in region {aws_region} with provided credentials", "cyan")
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Try to get account sending limits
        color_print("👉 Contacting AWS SES API...", "cyan")
        response = ses_client.get_send_quota()
        
        color_print("✅ AWS SES API credentials are valid!", "green")
        color_print(f"📊 Send quota: {response['Max24HourSend']} emails/24h", "green")
        color_print(f"📊 Emails sent: {response['SentLast24Hours']}", "green")
        color_print(f"📊 Max send rate: {response['MaxSendRate']} emails/sec", "green")
        
        return True
    except NoCredentialsError:
        color_print("❌ Invalid AWS credentials or credentials not found", "red")
        return False
    except ClientError as e:
        color_print(f"❌ AWS SES API error: {e.response['Error']['Code']} - {e.response['Error']['Message']}", "red")
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            color_print("👉 This suggests your AWS Access Key ID is invalid", "yellow")
        elif e.response['Error']['Code'] == 'SignatureDoesNotMatch':
            color_print("👉 This suggests your AWS Secret Access Key is invalid", "yellow")
        return False
    except Exception as e:
        color_print(f"❌ Unexpected error: {e}", "red")
        return False


def test_aws_ses_smtp_connection():
    """Test AWS SES SMTP connection"""
    color_print("\n📧 Testing AWS SES SMTP Connection...", "blue")
    
    # Get SMTP credentials from environment
    smtp_host = f"email-smtp.{os.environ.get('AWS_SES_REGION', 'eu-north-1')}.amazonaws.com"
    smtp_port = 587
    smtp_user = os.environ.get('AWS_SES_SMTP_USERNAME')
    smtp_pass = os.environ.get('AWS_SES_SMTP_PASSWORD')
    
    if not smtp_user or not smtp_pass:
        color_print("❌ No AWS SMTP credentials found in environment", "red")
        return False

    try:
        # Try to connect to the SMTP server
        color_print(f"👉 Connecting to SMTP server: {smtp_host}:{smtp_port}", "cyan")
        smtp = smtplib.SMTP(smtp_host, smtp_port)
        
        # Start TLS for security
        color_print("👉 Starting TLS...", "cyan")
        smtp.starttls()
        
        # Try to authenticate
        color_print("👉 Authenticating with SMTP server...", "cyan")
        smtp.login(smtp_user, smtp_pass)
        
        color_print("✅ SMTP connection and authentication successful!", "green")
        smtp.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        color_print("❌ SMTP authentication failed - invalid username or password", "red")
        return False
    except smtplib.SMTPException as e:
        color_print(f"❌ SMTP error: {str(e)}", "red")
        return False
    except Exception as e:
        color_print(f"❌ Unexpected error: {e}", "red")
        return False


def test_verified_email_addresses():
    """Test if the sender email is verified"""
    color_print("\n📧 Checking Verified Email Addresses...", "blue")
    
    # Get credentials from environment
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_SES_SMTP_USERNAME')    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY') or os.environ.get('AWS_SES_SMTP_PASSWORD')
    aws_region = os.environ.get('AWS_SES_REGION', 'eu-north-1')
    from_email = os.environ.get('AWS_SES_FROM_EMAIL', 'asadurzamannabin@gmail.com')
    
    if not aws_access_key or not aws_secret_key:
        color_print("❌ No AWS credentials found in environment", "red")
        return False
    
    try:
        # Create SES client
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Get verified email addresses
        response = ses_client.list_verified_email_addresses()
        verified_emails = response.get('VerifiedEmailAddresses', [])
        
        if not verified_emails:
            color_print("❌ No verified email addresses found", "red")
            color_print(f"👉 You need to verify {from_email} in the AWS SES console", "yellow")
            color_print(f"👉 Go to: https://{aws_region}.console.aws.amazon.com/ses/home?region={aws_region}#/verified-identities", "yellow")
            return False
        
        color_print(f"✅ Found {len(verified_emails)} verified email(s):", "green")
        for email in verified_emails:
            color_print(f"   - {email}", "green")
        
        if from_email in verified_emails:
            color_print(f"✅ Your sender email {from_email} is verified!", "green")
            return True
        else:
            color_print(f"❌ Your sender email {from_email} is NOT verified!", "red")
            color_print(f"👉 You must verify {from_email} in the AWS SES console", "yellow")
            color_print(f"👉 Go to: https://{aws_region}.console.aws.amazon.com/ses/home?region={aws_region}#/verified-identities", "yellow")
            return False
    except Exception as e:
        color_print(f"❌ Error checking verified emails: {e}", "red")
        return False


def test_send_email():
    """Test sending an email via AWS SES"""
    color_print("\n✉️ Testing Email Sending...", "blue")
    
    # Get credentials and settings
    smtp_host = f"email-smtp.{os.environ.get('AWS_SES_REGION', 'eu-north-1')}.amazonaws.com"
    smtp_port = 587    smtp_user = os.environ.get('AWS_SES_SMTP_USERNAME')
    smtp_pass = os.environ.get('AWS_SES_SMTP_PASSWORD')
    from_email = os.environ.get('AWS_SES_FROM_EMAIL', 'asadurzamannabin@gmail.com')
    
    # Ask for recipient email
    to_email = input("Enter recipient email (or press Enter to skip): ").strip()
    if not to_email:
        color_print("⏭️ Email sending test skipped", "yellow")
        return False
    
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = f'Scholarship Portal <{from_email}>'
        msg['To'] = to_email
        msg['Subject'] = 'AWS SES Test Email'
        
        body = """
        This is a test email sent from the Scholarship Portal application to verify AWS SES configuration.
        
        If you received this email, your AWS SES setup is working correctly!
        
        Time: {time}
        """
        
        msg.attach(MIMEText(body.format(time=sys.argv[0]), 'plain'))
        
        # Connect to SMTP server
        color_print("👉 Connecting to SMTP server...", "cyan")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        
        # Send email
        color_print("👉 Sending test email...", "cyan")
        server.send_message(msg)
        server.quit()
        
        color_print(f"✅ Test email sent successfully to {to_email}!", "green")
        return True
    except Exception as e:
        color_print(f"❌ Failed to send email: {e}", "red")
        return False


def main():
    """Run all tests"""
    color_print("🔍 AWS SES Credential Verification Script", "purple")
    color_print("===========================================", "purple")
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Print current settings
    color_print("\n⚙️ Current Settings:", "blue")
    color_print(f"👉 Region: {os.environ.get('AWS_SES_REGION', 'eu-north-1')}", "cyan")
    color_print(f"👉 SMTP Username: {os.environ.get('AWS_SES_SMTP_USERNAME', 'Not set')}", "cyan")
    color_print(f"👉 SMTP Password: {'*****' if os.environ.get('AWS_SES_SMTP_PASSWORD') else 'Not set'}", "cyan")
    color_print(f"👉 Sender Email: {os.environ.get('AWS_SES_FROM_EMAIL', 'Not set')}", "cyan")
    
    # Run tests
    results = {}
    results["API Credentials"] = test_aws_ses_api_credentials()
    results["SMTP Connection"] = test_aws_ses_smtp_connection()
    results["Verified Emails"] = test_verified_email_addresses()
    results["Send Email"] = test_send_email()
    
    # Print summary
    color_print("\n📋 Test Results Summary:", "purple")
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        color = "green" if result else "red"
        color_print(f"{test}: {status}", color)
    
    # Final verdict
    if all(results.values()):
        color_print("\n🎉 All tests passed! Your AWS SES configuration is working correctly.", "green")
    else:
        color_print("\n⚠️ Some tests failed. Please fix the issues before proceeding.", "red")
        
        if not results["API Credentials"]:
            color_print("👉 Check your AWS Access Key ID and Secret Access Key", "yellow")
        
        if not results["SMTP Connection"]:
            color_print("👉 Check your AWS SMTP credentials and region", "yellow")
        
        if not results["Verified Emails"]:
            color_print("👉 Verify your sender email in the AWS SES console", "yellow")
        
        if not results["Send Email"]:
            color_print("👉 Check if you're in the SES sandbox mode and can only send to verified emails", "yellow")


if __name__ == "__main__":
    main()
