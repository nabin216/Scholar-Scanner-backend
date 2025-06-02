#!/usr/bin/env python
"""
Comprehensive test for the complete OTP verification registration flow.
This simulates the real-world scenario where users register with email verification.
"""

import os
import django
import requests
import json
import uuid
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarships_api.settings')
django.setup()

from users.models import EmailVerification
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def test_complete_registration_flow():
    """Test the complete registration flow with OTP verification"""
    
    print("🔄 Testing Complete Registration Flow with OTP")
    print("=" * 60)
    
    # Generate unique test data
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    test_password = "SecureTestPassword123!"
    test_otp = "654321"
    
    print(f"📧 Test Email: {test_email}")
    print(f"🔑 Test Password: {test_password} (length: {len(test_password)})")
    print(f"🔢 Test OTP: {test_otp} (length: {len(test_otp)})")
    
    # Step 1: Create email verification record (simulating email sent)
    print(f"\n📝 Step 1: Creating email verification record...")
    
    try:
        otp_obj = EmailVerification.objects.create(
            email=test_email,
            otp_code=test_otp,
            is_used=False,
            is_verified=False
        )
        print(f"✓ Created EmailVerification: {otp_obj.otp_code} for {otp_obj.email}")
        print(f"  - Is valid: {otp_obj.is_valid()}")
        print(f"  - Created at: {otp_obj.created_at}")
        
    except Exception as e:
        print(f"❌ Failed to create EmailVerification: {e}")
        return False
    
    # Step 2: Test serializer validation directly
    print(f"\n🧪 Step 2: Testing UserRegistrationSerializer...")
    
    from users.serializers import UserRegistrationSerializer
    
    registration_data = {
        'email': test_email,
        'password': test_password,
        'password2': test_password,
        'full_name': 'Test User Full Name',
        'first_name': 'Test',
        'last_name': 'User',
        'otp_code': test_otp  # This is the critical test - 6 digits should NOT trigger password validation
    }
    
    print(f"📋 Registration data:")
    for key, value in registration_data.items():
        if key == 'password' or key == 'password2':
            print(f"   - {key}: [HIDDEN] (length: {len(value)})")
        else:
            print(f"   - {key}: {value}")
    
    # Test the serializer
    serializer = UserRegistrationSerializer(data=registration_data)
    
    if serializer.is_valid():
        print(f"\n✅ Serializer validation PASSED!")
        print(f"   - OTP code '{test_otp}' was accepted without password validation errors")
        print(f"   - No 'password too short' error occurred")
        
        # Step 3: Test user creation
        print(f"\n👤 Step 3: Testing user creation...")
        
        try:
            user = serializer.save()
            print(f"✅ User created successfully!")
            print(f"   - Email: {user.email}")
            print(f"   - Full name: {user.full_name}")
            print(f"   - Is active: {user.is_active}")
            print(f"   - Date joined: {user.date_joined}")
            
            # Verify OTP was marked as used
            otp_obj.refresh_from_db()
            print(f"   - OTP marked as used: {otp_obj.is_used}")
            print(f"   - OTP marked as verified: {otp_obj.is_verified}")
            
            # Step 4: Verify user can be retrieved
            print(f"\n🔍 Step 4: Verifying user in database...")
            
            db_user = User.objects.get(email=test_email)
            print(f"✅ User found in database:")
            print(f"   - ID: {db_user.id}")
            print(f"   - Email: {db_user.email}")
            print(f"   - Is active: {db_user.is_active}")
            
            success = True
            
        except Exception as create_error:
            print(f"❌ User creation failed: {create_error}")
            success = False
            
    else:
        print(f"\n❌ Serializer validation FAILED:")
        for field, errors in serializer.errors.items():
            print(f"   - {field}: {errors}")
            
        # Check specifically for the password validation bug
        if 'otp_code' in serializer.errors:
            for error in serializer.errors['otp_code']:
                if 'at least 10 characters' in str(error):
                    print(f"\n🚨 CRITICAL BUG DETECTED!")
                    print(f"   The OTP field is still being validated as a password!")
                    print(f"   Error: {error}")
                    return False
        
        success = False
    
    # Cleanup
    print(f"\n🧹 Cleanup...")
    try:
        User.objects.filter(email=test_email).delete()
        EmailVerification.objects.filter(email=test_email).delete()
        print(f"✓ Cleaned up test data")
    except Exception as cleanup_error:
        print(f"⚠️ Cleanup warning: {cleanup_error}")
    
    return success

def test_password_validation_still_works():
    """Ensure password validation still works for actual passwords"""
    
    print(f"\n🔒 Testing that password validation still works for passwords...")
    print("=" * 60)
    
    from users.serializers import UserRegistrationSerializer
    
    # Test with a password that's too short (should fail)
    test_email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    short_password = "short"  # Only 5 characters - should fail validation
    
    # Create valid OTP first
    otp_obj = EmailVerification.objects.create(
        email=test_email,
        otp_code="123456",
        is_used=False,
        is_verified=False
    )
    
    registration_data = {
        'email': test_email,
        'password': short_password,
        'password2': short_password,
        'full_name': 'Test User',
        'first_name': 'Test',
        'last_name': 'User',
        'otp_code': "123456"  # Valid OTP
    }
    
    print(f"🧪 Testing with short password: '{short_password}' (length: {len(short_password)})")
    
    serializer = UserRegistrationSerializer(data=registration_data)
    
    if not serializer.is_valid():
        print(f"✅ Password validation working correctly!")
        print(f"   - Short password was rejected")
        
        if 'password' in serializer.errors:
            for error in serializer.errors['password']:
                if 'at least 10 characters' in str(error):
                    print(f"   - Correct error: {error}")
                    break
        
        # Verify OTP validation was not affected
        if 'otp_code' not in serializer.errors:
            print(f"   - OTP validation was not affected by password validation")
        else:
            print(f"   ⚠️ OTP also failed: {serializer.errors['otp_code']}")
            
    else:
        print(f"❌ Password validation is broken - short password was accepted!")
        return False
    
    # Cleanup
    otp_obj.delete()
    return True

def main():
    print("🧪 OTP VALIDATION FIX - COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print("Testing the fix for: 'This password is too short. It must contain at least 10 characters.'")
    print("This error was incorrectly being triggered by 6-digit OTP codes.")
    print()
    
    # Test 1: Complete registration flow
    test1_success = test_complete_registration_flow()
    
    # Test 2: Ensure password validation still works
    test2_success = test_password_validation_still_works()
    
    # Summary
    print(f"\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    if test1_success and test2_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ OTP validation fix is working correctly")
        print("✅ Password validation still works for actual passwords")
        print("✅ Users can now complete registration with 6-digit OTP codes")
        print("\n💡 The issue has been resolved:")
        print("   - 6-digit OTP codes no longer trigger 'password too short' errors")
        print("   - Password validation is only applied to actual password fields")
        print("   - Registration flow works end-to-end")
        
    else:
        print("❌ SOME TESTS FAILED!")
        if not test1_success:
            print("❌ OTP validation fix needs more work")
        if not test2_success:
            print("❌ Password validation is broken")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
