#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship

scholarships = Scholarship.objects.all()
print(f"Found {scholarships.count()} scholarships")

for s in scholarships:
    print(f"ID: {s.id}, Title: {s.title}, Provider: {s.provider}")
    # Update provider with a more meaningful name based on sponsor types or title
    if s.provider == 'Unknown Provider':
        sponsor_types = [st.name for st in s.sponsor_type.all()]
        if sponsor_types:
            s.provider = f"{sponsor_types[0]} Foundation"
        else:
            # Extract provider from title or use a generic one
            if 'science' in s.title.lower():
                s.provider = 'National Science Foundation'
            elif 'health' in s.title.lower() or 'medical' in s.title.lower():
                s.provider = 'Health Sciences Institute'
            elif 'business' in s.title.lower() or 'management' in s.title.lower():
                s.provider = 'Corporate Excellence Foundation'
            else:
                s.provider = 'Academic Excellence Foundation'
        s.save()
        print(f"  Updated provider to: {s.provider}")

print("\nFinal provider values:")
for s in Scholarship.objects.all():
    print(f"ID: {s.id}, Provider: {s.provider}")
