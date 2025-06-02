#!/usr/bin/env python
"""
Simple email test with explicit print statements
"""

print("Starting email test...")

import os
import sys

# Load environment
print("Loading environment...")
from dotenv import load_dotenv
load_dotenv()

# Setup Django
print("Setting up Django...")
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')

import django
django.setup()

# Test imports
print("Testing imports...")
from django.conf import settings
from users.email_service import send_verification_email

print(f"Email Backend: {settings.EMAIL_BACKEND}")
print(f"AWS Access Key: {bool(os.getenv('AWS_ACCESS_KEY_ID'))}")
print(f"AWS Secret Key: {bool(os.getenv('AWS_SECRET_ACCESS_KEY'))}")
print(f"AWS Region: {os.getenv('AWS_SES_REGION')}")
print(f"From Email: {os.getenv('AWS_SES_FROM_EMAIL')}")

# Test email sending
print("\nTesting email sending...")
try:
    result = send_verification_email("expressbangla25@gmail.com", "123456")
    print(f"Email result: {result}")
    if result:
        print("✅ SUCCESS: Email sent!")
    else:
        print("❌ FAILED: Email not sent!")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("Test completed.")
