#!/usr/bin/env python
"""
Simple test script to verify email sending functionality.
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.append('.')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_django_email():
    """Test Django's email backend directly"""
    print("=== TESTING DJANGO EMAIL BACKEND ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        result = send_mail(
            subject='Test Email from Scholarship Portal',
            message='This is a test email to verify the email configuration.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['expressbangla25@gmail.com'],
            fail_silently=False,
        )
        print(f"✅ Django email sent successfully! Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Django email failed: {e}")
        return False

def test_aws_ses_api():
    """Test AWS SES API directly"""
    print("\n=== TESTING AWS SES API ===")
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError
        
        # Get AWS credentials
        aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        aws_region = os.environ.get('AWS_SES_REGION', 'eu-north-1')
        
        print(f"AWS_ACCESS_KEY_ID: {aws_access_key}")
        print(f"AWS_SECRET_ACCESS_KEY set: {bool(aws_secret_key)}")
        print(f"AWS_SES_REGION: {aws_region}")
        
        if not aws_access_key or not aws_secret_key:
            print("❌ AWS credentials not properly configured")
            return False
            
        # Create SES client
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        
        # Test sending email
        response = ses_client.send_email(
            Source=f'Scholarship Portal <{os.environ.get("AWS_SES_FROM_EMAIL")}>',
            Destination={
                'ToAddresses': ['expressbangla25@gmail.com'],
            },
            Message={
                'Subject': {
                    'Data': 'AWS SES API Test from Scholarship Portal',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': 'This is a test email sent via AWS SES API to verify the configuration.',
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        
        print(f"✅ AWS SES API email sent successfully! MessageId: {response['MessageId']}")
        return True
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"❌ AWS SES ClientError: {error_code} - {error_message}")
        
        if error_code == 'MessageRejected':
            print("💡 This usually means the sender email is not verified in AWS SES")
        elif error_code == 'InvalidParameterValue':
            print("💡 Check if your AWS credentials and region are correct")
        
        return False
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        return False
    except Exception as e:
        print(f"❌ AWS SES API failed: {e}")
        return False

def test_otp_email():
    """Test the OTP email function"""
    print("\n=== TESTING OTP EMAIL FUNCTION ===")
    try:
        from users.email_service import send_verification_email
        
        result = send_verification_email('expressbangla25@gmail.com', '123456')
        if result:
            print("✅ OTP email function returned success")
        else:
            print("❌ OTP email function returned failure")
        return result
    except Exception as e:
        print(f"❌ OTP email function failed: {e}")
        return False

if __name__ == "__main__":
    print("EMAIL TESTING SUITE")
    print("=" * 50)
    
    # Test 1: Django email backend
    django_result = test_django_email()
    
    # Test 2: AWS SES API
    aws_result = test_aws_ses_api()
    
    # Test 3: OTP email function
    otp_result = test_otp_email()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Django Email Backend: {'✅ PASS' if django_result else '❌ FAIL'}")
    print(f"AWS SES API: {'✅ PASS' if aws_result else '❌ FAIL'}")
    print(f"OTP Email Function: {'✅ PASS' if otp_result else '❌ FAIL'}")
    
    if not any([django_result, aws_result, otp_result]):
        print("\n🚨 ALL TESTS FAILED - EMAIL SYSTEM NOT WORKING")
    elif django_result or aws_result:
        print("\n✅ At least one email method is working")
    
    print("\n💡 RECOMMENDATIONS:")
    if not aws_result:
        print("- Verify that 'support@scholarscanner.com' is verified in AWS SES console")
        print("- Check if AWS SES is in sandbox mode (can only send to verified emails)")
    if not django_result:
        print("- Check SMTP credentials and settings")
    if not otp_result and (django_result or aws_result):
        print("- There may be an issue with the OTP email service logic")
