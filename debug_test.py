#!/usr/bin/env python
import os
import sys

print("Starting AWS SES test...")

try:
    from dotenv import load_dotenv
    print("✅ dotenv imported")
    
    load_dotenv()
    print("✅ Environment variables loaded")
    
    import boto3
    print("✅ boto3 imported")
    
    # Test environment variables
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_SES_REGION', 'eu-north-1')
    from_email = os.getenv('AWS_SES_FROM_EMAIL')
    
    print(f"AWS_ACCESS_KEY_ID: {aws_access_key[:10]}..." if aws_access_key else "Not set")
    print(f"AWS_SECRET_ACCESS_KEY: {'Set' if aws_secret_key else 'Not set'}")
    print(f"AWS_SES_REGION: {aws_region}")
    print(f"AWS_SES_FROM_EMAIL: {from_email}")
    
    if not aws_access_key or not aws_secret_key:
        print("❌ Missing AWS credentials")
        sys.exit(1)
    
    # Create SES client
    print("Creating SES client...")
    ses_client = boto3.client(
        'ses',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    print("✅ SES client created")
    
    # Test credentials
    print("Testing credentials...")
    quota = ses_client.get_send_quota()
    print(f"✅ Credentials valid. Daily limit: {quota['Max24HourSend']}")
    
    # Check verified emails
    print("Checking verified emails...")
    verified = ses_client.list_verified_email_addresses()
    verified_emails = verified.get('VerifiedEmailAddresses', [])
    print(f"Verified emails: {verified_emails}")
    
    if from_email not in verified_emails:
        print(f"⚠️  {from_email} is NOT verified!")
        print("You need to verify this email in AWS SES console")
    
    # Try sending email
    print(f"Sending test email...")
    response = ses_client.send_email(
        Source=from_email,
        Destination={'ToAddresses': ['expressbangla25@gmail.com']},
        Message={
            'Subject': {'Data': 'Test Email', 'Charset': 'UTF-8'},
            'Body': {
                'Text': {'Data': 'Test message', 'Charset': 'UTF-8'}
            }
        }
    )
    
    print(f"✅ EMAIL SENT! MessageId: {response['MessageId']}")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
