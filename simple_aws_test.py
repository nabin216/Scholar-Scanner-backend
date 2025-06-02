#!/usr/bin/env python
"""
Simple AWS SES test to verify credentials and email sending
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aws_ses_direct():
    """Test AWS SES API directly without Django"""
    print("=== AWS SES DIRECT TEST ===")
    
    # Get credentials from environment
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_SES_REGION', 'eu-north-1')
    from_email = os.getenv('AWS_SES_FROM_EMAIL')
    
    print(f"AWS_ACCESS_KEY_ID: {aws_access_key}")
    print(f"AWS_SECRET_ACCESS_KEY: {'***' + aws_secret_key[-4:] if aws_secret_key else 'Not set'}")
    print(f"AWS_SES_REGION: {aws_region}")
    print(f"AWS_SES_FROM_EMAIL: {from_email}")
    
    if not aws_access_key or not aws_secret_key:
        print("❌ AWS credentials not found in environment")
        return False
    
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        # Create SES client
        print("\n🔗 Creating SES client...")
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Test credentials by getting send quota
        print("🔍 Testing credentials...")
        quota = ses_client.get_send_quota()
        print(f"✅ Send quota: {quota['Max24HourSend']} emails per 24 hours")
        print(f"✅ Send rate: {quota['MaxSendRate']} emails per second")
        
        # Check verified email addresses
        print("\n📧 Checking verified email addresses...")
        verified_emails = ses_client.list_verified_email_addresses()
        print(f"Verified emails: {verified_emails.get('VerifiedEmailAddresses', [])}")
        
        if from_email not in verified_emails.get('VerifiedEmailAddresses', []):
            print(f"⚠️  WARNING: {from_email} is NOT verified in AWS SES!")
            print("   You need to verify this email address in the AWS SES console.")
            print("   In sandbox mode, you can only send TO verified email addresses.")
            
            # Check if account is in sandbox
            try:
                sending_enabled = ses_client.get_account_sending_enabled()
                print(f"   Account sending enabled: {sending_enabled.get('Enabled', False)}")
            except Exception as e:
                print(f"   Could not check account status: {e}")
        else:
            print(f"✅ {from_email} is verified in AWS SES")
        
        # Try sending a test email
        print(f"\n📬 Attempting to send test email to expressbangla25@gmail.com...")
        
        response = ses_client.send_email(
            Source=f'Scholarship Portal Test <{from_email}>',
            Destination={
                'ToAddresses': ['expressbangla25@gmail.com'],
            },
            Message={
                'Subject': {
                    'Data': 'AWS SES Test - Scholarship Portal',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'This is a test email to verify AWS SES configuration for the Scholarship Portal.',
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': '''
                        <html>
                        <body>
                            <h2>AWS SES Test - Scholarship Portal</h2>
                            <p>This is a test email to verify AWS SES configuration.</p>
                            <p>If you received this email, the AWS SES configuration is working!</p>
                            <p><strong>From:</strong> Scholarship Portal Email System</p>
                        </body>
                        </html>
                        ''',
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        print(f"✅ Email sent successfully! MessageId: {response['MessageId']}")
        print("📱 Check your inbox (and spam folder) for the test email.")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"❌ AWS SES ClientError: {error_code}")
        print(f"   Message: {error_message}")
        
        if error_code == 'MessageRejected':
            print("💡 This usually means:")
            print("   - Sender email is not verified in AWS SES")
            print("   - Account is in sandbox mode and recipient is not verified")
        elif error_code == 'InvalidParameterValue':
            print("💡 Check your AWS credentials and region settings")
        elif error_code == 'AccessDenied':
            print("💡 AWS credentials don't have SES permissions")
            
        return False
        
    except NoCredentialsError:
        print("❌ AWS credentials error - check your access key and secret key")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_aws_ses_direct()
