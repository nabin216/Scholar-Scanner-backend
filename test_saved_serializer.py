#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship
from users.models import SavedScholarship, User
from users.serializers import SavedScholarshipSerializer

# Check if we have any saved scholarships
saved_scholarships = SavedScholarship.objects.all()
print(f"Found {saved_scholarships.count()} saved scholarships")

if saved_scholarships.exists():
    # Test the serializer
    saved = saved_scholarships.first()
    serializer = SavedScholarshipSerializer(saved)
    data = serializer.data
    
    print("\nSaved scholarship data:")
    print(f"ID: {data.get('id')}")
    print(f"Scholarship ID: {data.get('scholarship')}")
    print(f"Date saved: {data.get('date_saved')}")
    
    # Check the scholarship_details field
    details = data.get('scholarship_details')
    if details:
        print(f"\nScholarship details:")
        print(f"  Title: {details.get('title')}")
        print(f"  Provider: {details.get('provider')}")
        print(f"  Amount: {details.get('amount')}")
        print(f"  Deadline: {details.get('deadline')}")
        print(f"  Description: {details.get('description', '')[:100]}...")
        
        if details.get('provider'):
            print("\n✅ Provider field is present and populated!")
        else:
            print("\n❌ Provider field is missing or empty")
    else:
        print("\n❌ scholarship_details field is missing")
        print(f"Available fields: {list(data.keys())}")
else:
    print("No saved scholarships found")
    
    # Check if we have any scholarships at all
    scholarships = Scholarship.objects.all()
    print(f"Total scholarships in database: {scholarships.count()}")
    
    if scholarships.exists():
        s = scholarships.first()
        print(f"Sample scholarship: {s.title}")
        print(f"Provider: {getattr(s, 'provider', 'NOT FOUND')}")
        print(f"Amount: {getattr(s, 'amount', 'NOT FOUND')}")
