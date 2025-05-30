#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import SavedScholarship, ScholarshipApplication
from scholarships.models import Scholarship

User = get_user_model()

def test_mark_as_applied_api():
    """Test the mark as applied functionality"""
    print("Testing Mark as Applied API functionality...")
    
    # Get a user with saved scholarships
    user = User.objects.filter(email='testuser@example.com').first()
    if not user:
        print("No test user found. Creating one...")
        user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            full_name='Test User'
        )
    
    # Get saved scholarships for this user
    saved_scholarships = SavedScholarship.objects.filter(user=user)
    print(f"User {user.email} has {saved_scholarships.count()} saved scholarships")
    
    if saved_scholarships.count() == 0:
        print("No saved scholarships found. Creating one for testing...")
        scholarship = Scholarship.objects.first()
        if scholarship:
            saved_scholarship = SavedScholarship.objects.create(
                user=user,
                scholarship=scholarship
            )
            print(f"Created saved scholarship: {saved_scholarship}")
        else:
            print("No scholarships available to save!")
            return
    
    # Test the API endpoints
    base_url = "http://localhost:8000/api/user"
    
    # First, let's get a token by logging in
    login_data = {
        'email': 'testuser@example.com',
        'password': 'testpass123'
    }
    
    try:
        # Login to get token
        login_response = requests.post(f"{base_url}/auth/login/", json=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('access')
            print(f"Successfully logged in, got token")
            
            headers = {'Authorization': f'Bearer {token}'}
            
            # Get saved scholarships
            saved_response = requests.get(f"{base_url}/saved-scholarships/", headers=headers)
            print(f"Saved scholarships response status: {saved_response.status_code}")
            
            if saved_response.status_code == 200:
                saved_data = saved_response.json()
                print(f"Found {len(saved_data.get('results', saved_data))} saved scholarships")
                
                # Get the first saved scholarship
                saved_scholarships_list = saved_data.get('results', saved_data)
                if saved_scholarships_list:
                    first_saved = saved_scholarships_list[0]
                    scholarship_id = first_saved['scholarship_details']['id']
                    saved_id = first_saved['id']
                    
                    print(f"Testing with scholarship ID: {scholarship_id}, saved ID: {saved_id}")
                    
                    # Create application
                    application_data = {
                        'scholarship': scholarship_id,
                        'status': 'pending',
                        'notes': 'Applied from saved scholarships via API test'
                    }
                    
                    app_response = requests.post(f"{base_url}/applications/", json=application_data, headers=headers)
                    print(f"Create application response status: {app_response.status_code}")
                    print(f"Create application response: {app_response.text}")
                    
                    if app_response.status_code in [200, 201]:
                        print("✅ Application created successfully!")
                        
                        # Remove from saved scholarships
                        delete_response = requests.delete(f"{base_url}/saved-scholarships/{saved_id}/", headers=headers)
                        print(f"Delete saved scholarship response status: {delete_response.status_code}")
                        
                        if delete_response.status_code in [200, 204]:
                            print("✅ Saved scholarship removed successfully!")
                            
                            # Verify application was created
                            apps_response = requests.get(f"{base_url}/applications/", headers=headers)
                            if apps_response.status_code == 200:
                                apps_data = apps_response.json()
                                apps_list = apps_data.get('results', apps_data)
                                print(f"User now has {len(apps_list)} applications")
                                
                                # Find our newly created application
                                for app in apps_list:
                                    if app.get('scholarship') == scholarship_id:
                                        print(f"✅ Found our application: {app['scholarship_title']} - Status: {app['status']}")
                                        break
                            
                            print("🎉 Mark as Applied functionality working correctly!")
                        else:
                            print(f"❌ Failed to remove saved scholarship: {delete_response.text}")
                    else:
                        print(f"❌ Failed to create application: {app_response.text}")
                else:
                    print("No saved scholarships to test with")
            else:
                print(f"Failed to get saved scholarships: {saved_response.text}")
        else:
            print(f"Login failed: {login_response.text}")
            
    except Exception as e:
        print(f"Error during API test: {e}")

if __name__ == '__main__':
    test_mark_as_applied_api()
