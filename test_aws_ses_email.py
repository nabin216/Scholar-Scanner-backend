import os
import sys
import django
import logging
from dotenv import load_dotenv
from colorama import init, Fore, Style

# Initialize colorama for colored terminal output
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Add the project directory to the Python path
sys.path.append('.')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

# Now import Django-related modules
from users.email_service import send_verification_email, send_welcome_email
from django.conf import settings

def color_print(message, color="white"):
    """Print colored messages in the terminal"""
    color_map = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
    }
    print(f"{color_map.get(color.lower(), Fore.WHITE)}{message}{Style.RESET_ALL}")

def test_verification_email():
    """Test sending a verification email"""
    color_print("\n===== TESTING VERIFICATION EMAIL =====", "blue")
    
    test_email = input("\nEnter an email address to send the verification email to: ")
    test_otp = "123456"  # Test OTP code
    
    color_print(f"\nSending verification email to {test_email} with OTP: {test_otp}", "cyan")
    
    result = send_verification_email(test_email, test_otp)
    
    if result:
        color_print("\n✅ Verification email sent successfully!", "green")
    else:
        color_print("\n❌ Failed to send verification email!", "red")
        
    return result

def test_welcome_email():
    """Test sending a welcome email"""
    color_print("\n===== TESTING WELCOME EMAIL =====", "blue")
    
    test_email = input("\nEnter an email address to send the welcome email to: ")
    test_name = input("Enter a name for the welcome email: ")
    
    color_print(f"\nSending welcome email to {test_email} with name: {test_name}", "cyan")
    
    # Create a simple mock user object
    class MockUser:
        def __init__(self, email, full_name):
            self.email = email
            self.full_name = full_name
    
    mock_user = MockUser(test_email, test_name)
    
    result = send_welcome_email(mock_user)
    
    if result:
        color_print("\n✅ Welcome email sent successfully!", "green")
    else:
        color_print("\n❌ Failed to send welcome email!", "red")
        
    return result

def check_aws_credentials():
    """Check if AWS credentials are properly set"""
    color_print("\n===== CHECKING AWS CREDENTIALS =====", "blue")
    
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_SES_REGION', 'eu-north-1')
    aws_from_email = os.environ.get('AWS_SES_FROM_EMAIL')
    
    color_print(f"AWS Access Key ID: {'✅ Set' if aws_access_key else '❌ Not set'}", "green" if aws_access_key else "red")
    color_print(f"AWS Secret Access Key: {'✅ Set' if aws_secret_key else '❌ Not set'}", "green" if aws_secret_key else "red")
    color_print(f"AWS SES Region: {aws_region}", "cyan")
    color_print(f"AWS SES From Email: {aws_from_email}", "cyan")
    
    # Check if the credentials are valid by initializing a boto3 client
    if aws_access_key and aws_secret_key:
        try:
            import boto3
            session = boto3.session.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=aws_region
            )
            ses_client = session.client('ses')
            
            # Check if the from_email is verified in SES
            if aws_from_email:
                try:
                    verified_emails = ses_client.list_verified_email_addresses()
                    if aws_from_email in verified_emails.get('VerifiedEmailAddresses', []):
                        color_print(f"✅ Your sender email {aws_from_email} is verified in AWS SES!", "green")
                    else:
                        color_print(f"❌ Your sender email {aws_from_email} is NOT verified in AWS SES!", "red")
                        color_print(f"👉 You need to verify {aws_from_email} in the AWS SES console", "yellow")
                except Exception as e:
                    color_print(f"Error checking verified emails: {str(e)}", "red")
            
            color_print("✅ AWS credentials are valid!", "green")
            return True
        except Exception as e:
            color_print(f"❌ AWS credentials test failed: {str(e)}", "red")
            return False
    else:
        color_print("❌ AWS credentials are not fully configured!", "red")
        return False

def main():
    """Main function to run the tests"""
    color_print("\n===== AWS SES EMAIL TESTER =====", "magenta")
    color_print("This script will test sending emails using AWS SES in your Django project.", "white")
    
    # Check AWS credentials
    aws_credentials_valid = check_aws_credentials()
    if not aws_credentials_valid:
        color_print("\n⚠️  AWS credentials are not valid or missing. The test will attempt to fall back to Django's email backend.", "yellow")
    
    # Show email backend configuration
    color_print(f"\nCurrent Email Backend: {settings.EMAIL_BACKEND}", "cyan")
    
    while True:
        color_print("\n===== TEST MENU =====", "magenta")
        color_print("1. Send Verification Email (OTP)")
        color_print("2. Send Welcome Email")
        color_print("3. Check AWS Credentials")
        color_print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            test_verification_email()
        elif choice == "2":
            test_welcome_email()
        elif choice == "3":
            check_aws_credentials()
        elif choice == "4":
            color_print("\nExiting...", "yellow")
            break
        else:
            color_print("\n❌ Invalid choice! Please enter a number from 1-4.", "red")

if __name__ == "__main__":
    main()
