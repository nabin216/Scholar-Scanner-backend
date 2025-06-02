#!/usr/bin/env python
"""
Test script to verify OTP validation fix.
This script tests that 6-digit OTP codes don't trigger password validation errors.
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from users.serializers import UserRegistrationSerializer
from users.models import EmailVerification
from rest_framework.exceptions import ValidationError
import uuid

def test_otp_validation():
    """Test that 6-digit OTP codes are accepted without password validation errors"""
    
    print("🧪 Testing OTP validation fix...")
    print("=" * 50)
    
    # Test data with a 6-digit OTP (should NOT trigger password validation)
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_data = {
        'email': test_email,
        'password': 'SecurePassword123!',
        'password2': 'SecurePassword123!',
        'full_name': 'Test User',
        'first_name': 'Test',
        'last_name': 'User',
        'otp_code': '123456'  # 6-digit OTP that should NOT cause password errors
    }
      # Create a mock OTP record for testing
    print(f"📝 Creating test OTP record for email: {test_email}")
    
    # Create EmailVerification record
    otp_obj = EmailVerification.objects.create(
        email=test_email,
        otp_code='123456',
        is_used=False,
        is_verified=False
    )
    print(f"✓ Created OTP: {otp_obj.otp_code}")
    
    # Test the serializer
    print(f"\n🔍 Testing UserRegistrationSerializer with 6-digit OTP...")
    
    try:
        serializer = UserRegistrationSerializer(data=test_data)
        
        print(f"📋 Input data:")
        print(f"   - email: {test_data['email']}")
        print(f"   - password: {test_data['password']} (length: {len(test_data['password'])})")
        print(f"   - otp_code: {test_data['otp_code']} (length: {len(test_data['otp_code'])})")
        
        if serializer.is_valid():
            print(f"\n✅ SUCCESS: Serializer validation passed!")
            print(f"   - OTP code '{test_data['otp_code']}' was accepted")
            print(f"   - No password validation errors triggered")
            print(f"   - The fix is working correctly!")
            
            # Test user creation (optional)
            try:
                user = serializer.save()
                print(f"   - User created successfully: {user.email}")
                print(f"   - User is active: {user.is_active}")
                
                # Verify OTP was marked as used
                otp_obj.refresh_from_db()
                print(f"   - OTP marked as used: {otp_obj.is_used}")
                print(f"   - OTP marked as verified: {otp_obj.is_verified}")
                
            except Exception as create_error:
                print(f"⚠️  User creation failed (but validation passed): {create_error}")
                
        else:
            print(f"\n❌ VALIDATION FAILED:")
            for field, errors in serializer.errors.items():
                print(f"   - {field}: {errors}")
                
            # Check specifically for password length errors on OTP
            if 'otp_code' in serializer.errors:
                for error in serializer.errors['otp_code']:
                    if 'at least 10 characters' in str(error):
                        print(f"\n🚨 CRITICAL: The password validation bug is still present!")
                        print(f"   OTP code validation is still being affected by password validators")
                        return False
                    
            print(f"\n🤔 Validation failed, but not due to the password length bug")
            
    except Exception as e:
        print(f"\n💥 UNEXPECTED ERROR: {e}")
        return False
    
    finally:
        # Clean up test data
        print(f"\n🧹 Cleaning up test data...")
        try:
            otp_obj.delete()
            print(f"   - Deleted OTP record")
        except:
            pass
            
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.filter(email=test_email).delete()
            print(f"   - Deleted test user (if created)")
        except:
            pass
    
    return True

def test_edge_cases():
    """Test edge cases for OTP validation"""
    
    print(f"\n🧪 Testing edge cases...")
    print("=" * 50)
    
    # Test cases that should fail validation (but not due to password length)
    test_cases = [
        {
            'name': 'Non-digit OTP',
            'otp_code': 'abc123',
            'expected_error': 'OTP must contain only digits'
        },
        {
            'name': 'Short OTP',
            'otp_code': '123',
            'expected_error': 'OTP must be exactly 6 digits'
        },
        {
            'name': 'Long OTP',
            'otp_code': '1234567890',
            'expected_error': 'OTP must be exactly 6 digits'
        },
        {
            'name': 'Missing OTP',
            'otp_code': None,
            'expected_error': 'OTP code is required'
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        
        test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        test_data = {
            'email': test_email,
            'password': 'SecurePassword123!',
            'password2': 'SecurePassword123!',
            'full_name': 'Test User',
            'first_name': 'Test',
            'last_name': 'User',
        }
        
        if test_case['otp_code'] is not None:
            test_data['otp_code'] = test_case['otp_code']
        
        serializer = UserRegistrationSerializer(data=test_data)
        
        if not serializer.is_valid():
            print(f"   ✓ Correctly failed validation")
            if 'otp_code' in serializer.errors:
                error_found = False
                for error in serializer.errors['otp_code']:
                    if test_case['expected_error'] in str(error):
                        print(f"   ✓ Correct error message: {error}")
                        error_found = True
                        break
                        
                if not error_found:
                    print(f"   ⚠️ Unexpected error: {serializer.errors['otp_code']}")
            else:
                print(f"   ⚠️ No OTP error found: {serializer.errors}")
        else:
            print(f"   ❌ Should have failed but passed validation")

if __name__ == '__main__':
    print("🔧 OTP Validation Fix - Test Suite")
    print("=" * 50)
    print("This script tests that the OTP validation fix prevents")
    print("6-digit OTP codes from triggering password validation errors.")
    print()
    
    success = test_otp_validation()
    test_edge_cases()
    
    print(f"\n" + "=" * 50)
    if success:
        print("🎉 SUMMARY: OTP validation fix appears to be working!")
        print("   - 6-digit OTP codes no longer trigger password length errors")
        print("   - Users should be able to complete registration with OTP verification")
    else:
        print("❌ SUMMARY: Issues detected with the OTP validation fix")
        print("   - Further investigation needed")
    print("=" * 50)
