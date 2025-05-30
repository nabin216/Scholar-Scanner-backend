#!/usr/bin/env python
import os
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship

scholarships = Scholarship.objects.all()
print(f"Updating amounts for {scholarships.count()} scholarships")

amounts = [5000, 10000, 15000, 20000, 25000, 30000]
for i, s in enumerate(scholarships):
    amount = Decimal(amounts[i % len(amounts)])
    s.amount = amount
    s.save()
    print(f"Updated {s.title[:50]}... with amount: ${amount}")

print("\nDone updating amounts")
