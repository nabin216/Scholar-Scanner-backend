#!/usr/bin/env python
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

from django.conf import settings

print("=== EMAIL CONFIGURATION DEBUG ===")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Not set')}")
print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Not set')}")
print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Not set')}")
print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Not set')}")
print(f"EMAIL_HOST_PASSWORD set: {bool(getattr(settings, 'EMAIL_HOST_PASSWORD', ''))}")
print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not set')}")

print("\n=== AWS SES CONFIGURATION ===")
print(f"AWS_SES_REGION: {getattr(settings, 'AWS_SES_REGION', 'Not set')}")
print(f"AWS_SES_FROM_EMAIL: {getattr(settings, 'AWS_SES_FROM_EMAIL', 'Not set')}")
print(f"AWS_ACCESS_KEY_ID set: {bool(getattr(settings, 'AWS_ACCESS_KEY_ID', ''))}")
print(f"AWS_SECRET_ACCESS_KEY set: {bool(getattr(settings, 'AWS_SECRET_ACCESS_KEY', ''))}")

print("\n=== ENVIRONMENT VARIABLES ===")
print(f"AWS_SES_SMTP_USERNAME: {os.environ.get('AWS_SES_SMTP_USERNAME', 'Not set')}")
print(f"AWS_SES_SMTP_PASSWORD set: {bool(os.environ.get('AWS_SES_SMTP_PASSWORD'))}")
print(f"AWS_ACCESS_KEY_ID: {os.environ.get('AWS_ACCESS_KEY_ID', 'Not set')}")
print(f"AWS_SECRET_ACCESS_KEY set: {bool(os.environ.get('AWS_SECRET_ACCESS_KEY'))}")
print(f"AWS_SES_REGION: {os.environ.get('AWS_SES_REGION', 'Not set')}")
print(f"AWS_SES_FROM_EMAIL: {os.environ.get('AWS_SES_FROM_EMAIL', 'Not set')}")

# Test email service import
try:
    from users.email_service import send_verification_email
    print("\n✅ Email service imported successfully")
except Exception as e:
    print(f"\n❌ Error importing email service: {e}")

# Test AWS SES availability
try:
    import boto3
    print("✅ boto3 is available")
except ImportError:
    print("❌ boto3 not available")
