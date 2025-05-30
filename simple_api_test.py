#!/usr/bin/env python
import requests
import json

def test_saved_scholarships_api():
    """Simple test to check the saved scholarships API response format"""
    
    # Test credentials
    login_url = "http://localhost:8000/api/user/auth/login/"
    login_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }
    
    # Login to get token
    print("1. Logging in...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        return
        
    login_result = login_response.json()
    token = login_result.get('access')
    print(f"✓ Login successful, token: {token[:20]}...")
    
    # Get saved scholarships
    print("\n2. Fetching saved scholarships...")
    headers = {"Authorization": f"Bearer {token}"}
    saved_response = requests.get("http://localhost:8000/api/user/saved-scholarships/", headers=headers)
    
    if saved_response.status_code != 200:
        print(f"Failed to fetch saved scholarships: {saved_response.status_code}")
        return
    
    saved_data = saved_response.json()
    print(f"✓ Found {len(saved_data)} saved scholarships")
      # Print first item structure
    if saved_data and len(saved_data) > 0:
        print("\n3. Sample saved scholarship structure:")
        print(json.dumps(saved_data[0], indent=2))
    else:
        print("No saved scholarships to display structure")
        print(f"API response type: {type(saved_data)}")
        print(f"API response: {saved_data}")

if __name__ == "__main__":
    test_saved_scholarships_api()
