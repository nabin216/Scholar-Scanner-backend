import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Load environment variables from .env file
load_dotenv()

def test_aws_credentials():
    """Test if AWS SES credentials are valid"""
    print("\n🔑 Testing AWS SES Credentials...")
    
    # Get credentials from .env file
    aws_username = os.environ.get('AWS_SES_SMTP_USERNAME')
    aws_password = os.environ.get('AWS_SES_SMTP_PASSWORD')
    aws_region = os.environ.get('AWS_SES_REGION')
    from_email = os.environ.get('AWS_SES_FROM_EMAIL')
    
    print(f"Region: {aws_region}")
    print(f"Username: {aws_username}")
    print(f"Password set: {bool(aws_password)}")
    print(f"From email: {from_email}")
    
    try:
        # Try to create an SES client
        print("\nCreating SES client...")
        ses_client = boto3.client(
            'ses',
            aws_access_key_id=aws_username,
            aws_secret_access_key=aws_password,
            region_name=aws_region
        )
        
        # Try to get account sending limits
        print("Getting account quota...")
        response = ses_client.get_send_quota()
        
        print(f"✅ Success! Daily quota: {response['Max24HourSend']}")
        
        # Check verified email addresses
        print("\nChecking verified emails...")
        verified_emails = ses_client.list_verified_email_addresses()
        
        print(f"Verified emails: {verified_emails['VerifiedEmailAddresses']}")
        
        if from_email in verified_emails['VerifiedEmailAddresses']:
            print(f"✅ Your sender email {from_email} is verified!")
        else:
            print(f"❌ Your sender email {from_email} is NOT verified!")
            print(f"You need to verify {from_email} in AWS SES console")
        
        return True
    except NoCredentialsError:
        print("❌ Invalid AWS credentials or credentials not found")
        print("Check your AWS_SES_SMTP_USERNAME and AWS_SES_SMTP_PASSWORD")
        return False
    except ClientError as e:
        print(f"❌ AWS SES API error: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        if e.response['Error']['Code'] == 'InvalidClientTokenId':
            print("This suggests your AWS Access Key ID is invalid")
        elif e.response['Error']['Code'] == 'SignatureDoesNotMatch':
            print("This suggests your AWS Secret Access Key is invalid")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_aws_credentials()
