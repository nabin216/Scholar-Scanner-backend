import os
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from scholarships.models import Scholarship

try:
    # Check API response
    response = requests.get('http://localhost:8000/api/scholarships/')
    print(f"API Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            first_scholarship = data['results'][0]
            print(f"API fields: {list(first_scholarship.keys())}")
            print(f"Title: {first_scholarship.get('title', 'N/A')}")
            print(f"Deadline: {first_scholarship.get('deadline', 'N/A')}")
            print(f"Open date: {first_scholarship.get('open_date', 'N/A')}")
            print(f"Created at: {first_scholarship.get('created_at', 'N/A')}")
            print(f"Country name: {first_scholarship.get('country_name', 'N/A')}")
        else:
            print("No scholarships in API response")
    else:
        print("API request failed")
        
except Exception as e:
    print(f"Error: {e}")
    
    # Check model directly
    scholarship = Scholarship.objects.first()
    if scholarship:
        print(f"Model fields: {[f.name for f in scholarship._meta.fields]}")
        print(f"Title: {scholarship.title}")
        print(f"Deadline: {scholarship.deadline}")
        print(f"Open date: {getattr(scholarship, 'open_date', 'N/A')}")
        print(f"Created at: {scholarship.created_at}")
        print(f"Country: {scholarship.country_detail.name if scholarship.country_detail else 'N/A'}")
    else:
        print("No scholarships in database")
