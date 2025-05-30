import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import *
from datetime import date, timedelta

# Create more sample scholarships
scholarships_data = [
    {
        'title': 'STEM Innovation Grant',
        'description': 'Supporting innovative research in Science, Technology, Engineering, and Mathematics.',
        'provider': 'National Science Foundation',
        'amount': 20000.00,
    },
    {
        'title': 'Business Leadership Award', 
        'description': 'For students demonstrating exceptional leadership in business.',
        'provider': 'Corporate Excellence Foundation',
        'amount': 10000.00,
    },
    {
        'title': 'Medical Research Grant',
        'description': 'Supporting future medical professionals and researchers.',
        'provider': 'Health Sciences Institute', 
        'amount': 25000.00,
    },
    {
        'title': 'Community Service Scholarship',
        'description': 'Recognizing students who make a difference in their communities.',
        'provider': 'Civic Engagement Alliance',
        'amount': 5000.00,
    }
]

usa, _ = Country.objects.get_or_create(name='United States')

for data in scholarships_data:
    s, created = Scholarship.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'provider': data['provider'], 
            'amount': data['amount'],
            'country': usa,
            'deadline': date.today() + timedelta(days=90),
            'application_url': f'https://example.com/apply/{data["title"].lower().replace(" ", "-")}',
        }
    )
    print(f'Scholarship "{data["title"]}": {"created" if created else "already exists"}')

print(f'Total scholarships: {Scholarship.objects.count()}')
