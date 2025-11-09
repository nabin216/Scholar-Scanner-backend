import requests
import json

# Test the saved scholarships API endpoint
def test_saved_scholarships_api():
    print("Testing saved scholarships API...")
    
    # First, let's try to get a valid token by logging in
    login_url = "http://127.0.0.1:8000/api/user/login/"
    
    # You'll need to replace these with actual user credentials
    # For now, let's just test the endpoint without auth to see the response
    saved_url = "http://127.0.0.1:8000/api/user/saved-scholarships/"
    
    print(f"Testing endpoint: {saved_url}")
    
    try:
        # Test without authentication first to see what error we get
        response = requests.get(saved_url)
        print(f"Status Code (no auth): {response.status_code}")
        print(f"Response (no auth): {response.text}")
        
        # If you have a valid token, uncomment and modify this:
        # headers = {"Authorization": "Bearer YOUR_TOKEN_HERE"}
        # response = requests.get(saved_url, headers=headers)
        # print(f"Status Code (with auth): {response.status_code}")
        # print(f"Response (with auth): {response.json()}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_saved_scholarships_api()
