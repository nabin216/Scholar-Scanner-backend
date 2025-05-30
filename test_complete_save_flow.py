#!/usr/bin/env python3
"""
Test script to verify the save scholarship functionality works end-to-end
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_user_registration_and_save():
    """Test user registration and scholarship saving functionality"""
    
    # Test data
    test_user = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "password2": "testpassword123",
        "full_name": "Test User",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("=== Testing Save Scholarship Functionality ===\n")
    
    # Step 1: Register a test user
    print("1. Registering test user...")
    try:
        register_response = requests.post(
            f"{BASE_URL}/user/auth/register/",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if register_response.status_code == 201:
            print("✓ User registration successful")
            user_data = register_response.json()
        elif register_response.status_code == 400:
            # User might already exist, try to login
            print("User already exists, attempting login...")
            login_response = requests.post(
                f"{BASE_URL}/user/auth/login/",
                json={"email": test_user["email"], "password": test_user["password"]},
                headers={"Content-Type": "application/json"}
            )
            
            if login_response.status_code == 200:
                print("✓ User login successful")
                user_data = login_response.json()
            else:
                print(f"✗ Login failed: {login_response.status_code}")
                print(login_response.text)
                return
        else:
            print(f"✗ Registration failed: {register_response.status_code}")
            print(register_response.text)
            return
            
    except Exception as e:
        print(f"✗ Registration/Login error: {e}")
        return
    
    # Extract token
    token = user_data.get('access') or user_data.get('token')
    if not token:
        print("✗ No authentication token received")
        return
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    # Step 2: Get list of scholarships
    print("\n2. Fetching scholarships...")
    try:
        scholarships_response = requests.get(f"{BASE_URL}/scholarships/")
        
        if scholarships_response.status_code == 200:
            scholarships = scholarships_response.json()
            print(f"✓ Found {len(scholarships)} scholarships")
            
            if len(scholarships) == 0:
                print("✗ No scholarships found to test with")
                return
                
            # Use the first scholarship for testing
            test_scholarship = scholarships[0]
            scholarship_id = test_scholarship['id']
            print(f"✓ Using scholarship: {test_scholarship['title']}")
        else:
            print(f"✗ Failed to fetch scholarships: {scholarships_response.status_code}")
            return
            
    except Exception as e:
        print(f"✗ Error fetching scholarships: {e}")
        return
    
    # Step 3: Save the scholarship
    print(f"\n3. Saving scholarship (ID: {scholarship_id})...")
    try:
        save_data = {"scholarship": scholarship_id}
        save_response = requests.post(
            f"{BASE_URL}/user/saved-scholarships/",
            json=save_data,
            headers=headers
        )
        
        if save_response.status_code in [200, 201]:
            print("✓ Scholarship saved successfully")
            saved_data = save_response.json()
            print(f"  Saved on: {saved_data.get('date_saved')}")
        else:
            print(f"✗ Failed to save scholarship: {save_response.status_code}")
            print(save_response.text)
            return
            
    except Exception as e:
        print(f"✗ Error saving scholarship: {e}")
        return
    
    # Step 4: Verify the scholarship was saved by fetching saved scholarships
    print("\n4. Verifying saved scholarships...")
    try:
        saved_response = requests.get(
            f"{BASE_URL}/user/saved-scholarships/",
            headers=headers
        )
        
        if saved_response.status_code == 200:
            saved_scholarships = saved_response.json()
            print(f"✓ Found {len(saved_scholarships)} saved scholarships")
            
            # Check if our scholarship is in the list
            scholarship_found = False
            for saved in saved_scholarships:
                if saved['scholarship'] == scholarship_id:
                    scholarship_found = True
                    print(f"✓ Verified: {saved['scholarship_details']['title']} is saved")
                    break
            
            if not scholarship_found:
                print("✗ Scholarship not found in saved list")
            
        else:
            print(f"✗ Failed to fetch saved scholarships: {saved_response.status_code}")
            return
            
    except Exception as e:
        print(f"✗ Error fetching saved scholarships: {e}")
        return
    
    # Step 5: Test duplicate save (should not create duplicate)
    print(f"\n5. Testing duplicate save prevention...")
    try:
        duplicate_save_response = requests.post(
            f"{BASE_URL}/user/saved-scholarships/",
            json=save_data,
            headers=headers
        )
        
        if duplicate_save_response.status_code in [200, 201]:
            print("✓ Duplicate save handled correctly")
        else:
            print(f"? Unexpected response for duplicate save: {duplicate_save_response.status_code}")
            
    except Exception as e:
        print(f"✗ Error testing duplicate save: {e}")
    
    # Step 6: Test unsaving the scholarship
    print(f"\n6. Testing unsave functionality...")
    try:
        # First, get the saved scholarship ID
        saved_response = requests.get(f"{BASE_URL}/user/saved-scholarships/", headers=headers)
        saved_scholarships = saved_response.json()
        
        saved_scholarship_id = None
        for saved in saved_scholarships:
            if saved['scholarship'] == scholarship_id:
                saved_scholarship_id = saved['id']
                break
        
        if saved_scholarship_id:
            unsave_response = requests.delete(
                f"{BASE_URL}/user/saved-scholarships/{saved_scholarship_id}/",
                headers=headers
            )
            
            if unsave_response.status_code == 204:
                print("✓ Scholarship unsaved successfully")
            else:
                print(f"✗ Failed to unsave scholarship: {unsave_response.status_code}")
        else:
            print("✗ Could not find saved scholarship ID for unsaving")
            
    except Exception as e:
        print(f"✗ Error unsaving scholarship: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_user_registration_and_save()
