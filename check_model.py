#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship

s = Scholarship.objects.first()
if s:
    print("Available fields:")
    print([field.name for field in s._meta.fields])
    print(f"\nFirst scholarship data:")
    print(f"Title: {s.title}")
    print(f"Sponsor types: {[st.name for st in s.sponsor_type.all()]}")
    print(f"Has provider field: {hasattr(s, 'provider')}")
else:
    print("No scholarships found")
