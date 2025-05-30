#!/usr/bin/env python
import requests
import json

# Test the saved scholarships API
token = "your_auth_token_here"  # You'll need to get this from localStorage

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

try:
    response = requests.get('http://localhost:8000/api/user/saved-scholarships/', headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Sample saved scholarship data:")
        if data.get('results'):
            scholarship = data['results'][0]
            details = scholarship.get('scholarship_details', {})
            print(f"Title: {details.get('title')}")
            print(f"Provider: {details.get('provider')}")
            print(f"Amount: {details.get('amount')}")
            print(f"Deadline: {details.get('deadline')}")
        else:
            print("No saved scholarships found")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection error: {e}")
    print("Note: You need to add a valid auth token to test this")
