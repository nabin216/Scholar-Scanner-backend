#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import SavedScholarship
from scholarships.models import Scholarship

User = get_user_model()

def test_saved_scholarship_functionality():
    print("Testing Save Scholarship functionality...")
    
    # Create or get a test user
    test_email = "testuser@example.com"
    user, created = User.objects.get_or_create(
        email=test_email,
        defaults={
            'full_name': 'Test User',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpassword123')
        user.save()
        print(f"Created test user: {user.email}")
    else:
        print(f"Using existing test user: {user.email}")
    
    # Get first scholarship
    scholarship = Scholarship.objects.first()
    if not scholarship:
        print("No scholarships found in database!")
        return
    
    print(f"Testing with scholarship: {scholarship.title}")
    
    # Test creating a saved scholarship
    saved_scholarship, created = SavedScholarship.objects.get_or_create(
        user=user,
        scholarship=scholarship
    )
    
    if created:
        print(f"✓ Successfully saved scholarship for user")
    else:
        print(f"✓ Scholarship was already saved for user")
    
    # Test the serializer
    from users.serializers import SavedScholarshipSerializer
    serializer = SavedScholarshipSerializer(saved_scholarship)
    data = serializer.data
    
    print(f"✓ Serializer data structure:")
    print(f"  - ID: {data['id']}")
    print(f"  - User: {data['user']}")
    print(f"  - Scholarship ID: {data['scholarship']}")
    print(f"  - Date Saved: {data['date_saved']}")
    print(f"  - Has scholarship_details: {'scholarship_details' in data}")
    
    if 'scholarship_details' in data:
        details = data['scholarship_details']
        print(f"  - Scholarship Title: {details.get('title')}")
        print(f"  - Provider: {details.get('provider')}")
        print(f"  - Amount: {details.get('amount')}")
        print(f"  - Country: {details.get('country')}")
    
    print(f"\nTotal saved scholarships for {user.email}: {SavedScholarship.objects.filter(user=user).count()}")
    print("✓ Save Scholarship functionality test completed successfully!")

if __name__ == '__main__':
    test_saved_scholarship_functionality()
