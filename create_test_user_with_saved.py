#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from scholarships.models import Scholarship
from users.models import SavedScholarship

User = get_user_model()

# Create a test user if it doesn't exist
user, created = User.objects.get_or_create(
    email='test@example.com',
    defaults={
        'first_name': 'Test',
        'last_name': 'User',
        'full_name': 'Test User'
    }
)

if created:
    user.set_password('testpassword123')
    user.save()
    print(f"Created test user: {user.email}")
else:
    print(f"Using existing user: {user.email}")

# Get some scholarships
scholarships = Scholarship.objects.all()[:3]
print(f"Found {scholarships.count()} scholarships")

# Save them for the test user
for scholarship in scholarships:
    saved, created = SavedScholarship.objects.get_or_create(
        user=user,
        scholarship=scholarship
    )
    if created:
        print(f"Saved scholarship: {scholarship.title}")
    else:
        print(f"Already saved: {scholarship.title}")

print(f"\nTest user now has {SavedScholarship.objects.filter(user=user).count()} saved scholarships")

# Test the serialization
from users.serializers import SavedScholarshipSerializer
saved_scholarships = SavedScholarship.objects.filter(user=user)

for saved in saved_scholarships[:1]:  # Just test the first one
    serializer = SavedScholarshipSerializer(saved)
    data = serializer.data
    
    print(f"\nTesting serialization for: {saved.scholarship.title}")
    details = data.get('scholarship_details')
    if details:
        print(f"✅ scholarship_details found")
        print(f"  Provider: {details.get('provider')}")
        print(f"  Amount: {details.get('amount')}")
        print(f"  Title: {details.get('title')}")
        print(f"  Deadline: {details.get('deadline')}")
    else:
        print(f"❌ scholarship_details missing")
        print(f"Available fields: {list(data.keys())}")

print(f"\nUser ID: {user.id}")
print(f"You can login with: {user.email} / testpassword123")
