#!/usr/bin/env python
import os
import sys
import requests
import json
from datetime import datetime

# Setup Django environment
import django
sys.path.append('d:/ScholarshipPortal/scholarship-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import SavedScholarship
from scholarships.models import Scholarship

User = get_user_model()

def test_complete_save_flow():
    """Test the complete save for later functionality"""
    
    print("=== DEBUGGING SAVE FOR LATER FUNCTIONALITY ===")
    
    # Test data
    test_email = "testuser@example.com"
    test_password = "TestPassword123!"
    
    # Step 1: Create or get test user
    print("\n1. Setting up test user...")
    user, created = User.objects.get_or_create(
        email=test_email,
        defaults={
            'full_name': 'Test User',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password(test_password)
        user.save()
        print(f"Created new user: {user.email}")
    else:
        print(f"Using existing user: {user.email}")
    
    # Step 2: Check available scholarships
    print("\n2. Checking available scholarships...")
    scholarships = Scholarship.objects.all()
    print(f"Total scholarships in database: {scholarships.count()}")
    
    if scholarships.count() == 0:
        print("ERROR: No scholarships found in database!")
        return
    
    test_scholarship = scholarships.first()
    print(f"Using test scholarship: {test_scholarship.title} (ID: {test_scholarship.id})")
    
    # Step 3: Test login API
    print("\n3. Testing login API...")
    login_url = "http://localhost:8000/api/user/auth/login/"
    login_data = {
        "email": test_email,
        "password": test_password
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            print("Login successful!")
            
            # Get token
            token = login_result.get('access') or login_result.get('token')
            if token:
                print(f"Token obtained: {token[:20]}...")
            else:
                print("ERROR: No token in login response!")
                print(f"Login response: {login_result}")
                return
        else:
            print(f"Login failed: {login_response.text}")
            return
            
    except Exception as e:
        print(f"Login request failed: {e}")
        return
    
    # Step 4: Test save scholarship API
    print("\n4. Testing save scholarship API...")
    save_url = "http://localhost:8000/api/user/saved-scholarships/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    save_data = {
        "scholarship": test_scholarship.id
    }
    
    try:
        save_response = requests.post(save_url, json=save_data, headers=headers)
        print(f"Save response status: {save_response.status_code}")
        print(f"Save response: {save_response.text}")
        
        if save_response.status_code in [200, 201]:
            print("Save successful!")
        else:
            print(f"Save failed: {save_response.text}")
            
    except Exception as e:
        print(f"Save request failed: {e}")
    
    # Step 5: Check database directly
    print("\n5. Checking database directly...")
    saved_count = SavedScholarship.objects.filter(user=user).count()
    print(f"Saved scholarships for user {user.email}: {saved_count}")
    
    if saved_count > 0:
        saved_scholarships = SavedScholarship.objects.filter(user=user)
        for saved in saved_scholarships:
            print(f"  - {saved.scholarship.title} (saved on {saved.date_saved})")
    
    # Step 6: Test get saved scholarships API
    print("\n6. Testing get saved scholarships API...")
    try:
        get_response = requests.get(save_url, headers=headers)
        print(f"Get saved response status: {get_response.status_code}")
        
        if get_response.status_code == 200:
            saved_data = get_response.json()
            print(f"API returned {len(saved_data)} saved scholarships")
            
            if len(saved_data) > 0:
                print("Saved scholarships from API:")
                for item in saved_data:
                    scholarship_details = item.get('scholarship_details', {})
                    print(f"  - {scholarship_details.get('title', 'Unknown')} (ID: {item.get('scholarship')})")
            else:
                print("No saved scholarships returned from API")
        else:
            print(f"Get saved failed: {get_response.text}")
            
    except Exception as e:
        print(f"Get saved request failed: {e}")
    
    # Step 7: Check user authentication endpoint
    print("\n7. Testing user authentication endpoint...")
    me_url = "http://localhost:8000/api/user/auth/me/"
    try:
        me_response = requests.get(me_url, headers=headers)
        print(f"Me response status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_data = me_response.json()
            print(f"Authenticated user: {user_data.get('email')} (ID: {user_data.get('id')})")
        else:
            print(f"Authentication check failed: {me_response.text}")
            
    except Exception as e:
        print(f"Me request failed: {e}")
    
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    test_complete_save_flow()
