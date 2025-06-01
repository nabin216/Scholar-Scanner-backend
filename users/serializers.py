from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from .models import UserProfile, SavedScholarship, ScholarshipApplication, EmailVerification

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'education', 'phone_number', 'address', 'date_of_birth', 'profile_picture']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'first_name', 'last_name', 'profile', 'date_joined']
        read_only_fields = ['date_joined']
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields
        profile = instance.profile
        if profile and profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for email verification request"""
    email = serializers.EmailField(required=True)


class OTPVerificationSerializer(serializers.Serializer):
    """Serializer for OTP verification"""
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(max_length=6, required=True)
    
    def validate_otp_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only digits")
        if len(value) != 6:
            raise serializers.ValidationError("OTP must be 6 digits")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration with email verification"""
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    otp_code = serializers.CharField(max_length=6, required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'full_name', 'first_name', 'last_name', 'otp_code']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Verify OTP
        email = attrs['email']
        otp_code = attrs['otp_code']
        
        try:
            otp_obj = EmailVerification.objects.filter(
                email=email,
                otp_code=otp_code,
                is_used=False,
                is_verified=False
            ).latest('created_at')
            
            if not otp_obj.is_valid():
                raise serializers.ValidationError({"otp_code": "Invalid or expired OTP code."})
                
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError({"otp_code": "Invalid OTP code."})
        
        return attrs
    
    def create(self, validated_data):
        # Remove OTP and password2 from validated_data
        otp_code = validated_data.pop('otp_code')
        validated_data.pop('password2')
        
        # Mark OTP as used and verified
        otp_obj = EmailVerification.objects.filter(
            email=validated_data['email'],
            otp_code=otp_code,
            is_used=False
        ).latest('created_at')
        otp_obj.is_used = True
        otp_obj.is_verified = True
        otp_obj.save()
        
        # Create user with verified email
        user = User.objects.create_user(**validated_data)
        user.is_active = True  # Account is verified
        user.save()
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class SavedScholarshipSerializer(serializers.ModelSerializer):
    """Serializer for saved scholarships"""
    
    scholarship_title = serializers.CharField(source='scholarship.title', read_only=True)
    scholarship_provider = serializers.CharField(source='scholarship.provider', read_only=True)
    scholarship_amount = serializers.DecimalField(
        source='scholarship.amount', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    scholarship_deadline = serializers.DateField(source='scholarship.deadline', read_only=True)
    
    # Add the full scholarship details object
    scholarship_details = serializers.SerializerMethodField()

    def get_scholarship_details(self, obj):
        """Return the full scholarship details"""
        from scholarships.serializers import ScholarshipSerializer
        return ScholarshipSerializer(obj.scholarship).data

    class Meta:
        model = SavedScholarship
        fields = [
            'id', 'user', 'scholarship', 'date_saved', 'scholarship_title',
            'scholarship_provider', 'scholarship_amount', 'scholarship_deadline',
            'scholarship_details'
        ]
        read_only_fields = ['user', 'date_saved']


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    """Serializer for scholarship applications"""
    
    scholarship_title = serializers.CharField(source='scholarship.title', read_only=True)
    scholarship_provider = serializers.CharField(source='scholarship.provider', read_only=True)
    scholarship_amount = serializers.DecimalField(
        source='scholarship.amount', 
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )
    
    class Meta:
        model = ScholarshipApplication
        fields = [
            'id', 'user', 'scholarship', 'status', 'date_applied', 'last_updated',
            'notes', 'scholarship_title', 'scholarship_provider', 'scholarship_amount'
        ]
        read_only_fields = ['user', 'date_applied', 'last_updated']
