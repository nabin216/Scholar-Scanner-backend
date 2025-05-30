#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship, SponsorType

print("Available sponsor types:")
for st in SponsorType.objects.all():
    print(f"- {st.name}")

print("\nSample scholarship with sponsor types:")
s = Scholarship.objects.first()
if s:
    print(f"Title: {s.title}")
    print(f"Sponsor types: {[st.name for st in s.sponsor_type.all()]}")
