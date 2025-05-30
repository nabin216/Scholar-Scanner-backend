#!/usr/bin/env python3

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/user/auth/login/"
APPLICATIONS_URL = f"{BASE_URL}/api/user/applications/"

# Test credentials - adjust these if needed
username = "testuser"  # Update with actual test user
password = "testpass123"

def test_status_update():
    # First, login to get a token
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        login_response = requests.post(LOGIN_URL, json=login_data)
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token = login_response.json().get('access')
        if not token:
            print("No access token received")
            return
        
        print(f"Login successful, token received")
        
        # Get all applications
        headers = {'Authorization': f'Bearer {token}'}
        apps_response = requests.get(APPLICATIONS_URL, headers=headers)
        
        if apps_response.status_code != 200:
            print(f"Failed to fetch applications: {apps_response.status_code}")
            return
        
        applications = apps_response.json().get('results', [])
        print(f"Found {len(applications)} applications")
        
        if not applications:
            print("No applications found to test with")
            return
        
        # Test updating the first application's status
        app = applications[0]
        app_id = app['id']
        current_status = app['status']
        
        print(f"Testing status update for application {app_id}")
        print(f"Current status: {current_status}")
        
        # Change to a different status
        new_status = 'approved' if current_status != 'approved' else 'rejected'
        
        update_url = f"{APPLICATIONS_URL}{app_id}/"
        update_data = {'status': new_status}
        
        update_response = requests.patch(update_url, json=update_data, headers=headers)
        
        if update_response.status_code == 200:
            updated_app = update_response.json()
            print(f"✅ Status update successful!")
            print(f"New status: {updated_app['status']}")
        else:
            print(f"❌ Status update failed: {update_response.status_code}")
            print(f"Response: {update_response.text}")
            
    except Exception as e:
        print(f"Error during test: {str(e)}")

if __name__ == "__main__":
    test_status_update()
