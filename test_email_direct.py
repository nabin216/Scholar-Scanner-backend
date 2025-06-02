#!/usr/bin/env python
"""
Simple test of the email verification system with proper Django setup
"""

import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

# Now import Django modules
from users.email_service import send_verification_email
from django.conf import settings
import logging

# Configure logging to show more details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_email_verification():
    """Test the email verification system"""
    print("=== EMAIL VERIFICATION TEST ===")
    print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    print(f"AWS_SES_REGION: {getattr(settings, 'AWS_SES_REGION', 'Not set')}")
    print(f"AWS_SES_FROM_EMAIL: {getattr(settings, 'AWS_SES_FROM_EMAIL', 'Not set')}")
    
    test_email = "expressbangla25@gmail.com"
    test_otp = "123456"
    
    print(f"\nSending verification email to: {test_email}")
    print(f"OTP Code: {test_otp}")
    
    try:
        result = send_verification_email(test_email, test_otp)
        
        if result:
            print("✅ Email sent successfully!")
            print("📧 Check your inbox and spam folder")
        else:
            print("❌ Email sending failed")
            
        return result
        
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_email_verification()
