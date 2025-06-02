#!/usr/bin/env python
"""
Test the email verification API endpoint directly
"""

import requests
import json

def test_email_verification_api():
    """Test the email verification endpoint"""
    print("=== TESTING EMAIL VERIFICATION API ===")
    
    # API endpoint
    url = "http://localhost:8000/api/auth/send-verification-email/"
    
    # Test data
    data = {
        "email": "expressbangla25@gmail.com"
    }
    
    print(f"Making POST request to: {url}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_json = response.json()
            print(f"Response JSON: {json.dumps(response_json, indent=2)}")
        except json.JSONDecodeError:
            print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ API call successful")
        else:
            print(f"❌ API call failed with status {response.status_code}")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Django server")
        print("Make sure Django server is running on port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_email_verification_api()
