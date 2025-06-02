#!/usr/bin/env python
"""
Email test with file output
"""

import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')

import django
django.setup()

from django.conf import settings
from users.email_service import send_verification_email
import traceback

# Write results to file
with open('email_test_results.txt', 'w') as f:
    f.write("=== EMAIL VERIFICATION TEST RESULTS ===\n\n")
    
    f.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}\n")
    f.write(f"AWS_ACCESS_KEY_ID set: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}\n")
    f.write(f"AWS_SECRET_ACCESS_KEY set: {bool(os.getenv('AWS_SECRET_ACCESS_KEY'))}\n")
    f.write(f"AWS_SES_REGION: {os.getenv('AWS_SES_REGION')}\n")
    f.write(f"AWS_SES_FROM_EMAIL: {os.getenv('AWS_SES_FROM_EMAIL')}\n\n")
    
    f.write("Testing email verification...\n")
    
    try:
        result = send_verification_email("expressbangla25@gmail.com", "123456")
        f.write(f"Email sending result: {result}\n")
        
        if result:
            f.write("✅ SUCCESS: Verification email sent successfully!\n")
            f.write("Check your inbox and spam folder for the email.\n")
        else:
            f.write("❌ FAILED: Email verification function returned False\n")
            f.write("This indicates the email was not sent successfully.\n")
            
    except Exception as e:
        f.write(f"❌ EXCEPTION: {str(e)}\n")
        f.write("Full traceback:\n")
        f.write(traceback.format_exc())
    
    f.write("\nTest completed.\n")

print("Email test completed. Check email_test_results.txt for results.")
