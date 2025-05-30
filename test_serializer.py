#!/usr/bin/env python
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship
from scholarships.serializers import ScholarshipSerializer

# Test that ScholarshipSerializer now includes provider and amount
s = Scholarship.objects.first()
if s:
    serializer = ScholarshipSerializer(s)
    data = serializer.data
    
    print("Scholarship serialized data:")
    print(f"Title: {data.get('title')}")
    print(f"Provider: {data.get('provider')}")
    print(f"Amount: {data.get('amount')}")
    print(f"Deadline: {data.get('deadline')}")
    print(f"\nAll fields: {list(data.keys())}")
    
    # Check if provider field exists
    if 'provider' in data:
        print(f"\n✅ Provider field is present: {data['provider']}")
    else:
        print("\n❌ Provider field is missing")
else:
    print("No scholarships found")
