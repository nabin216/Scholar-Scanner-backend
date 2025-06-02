from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import string
from datetime import timedelta
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with email as the unique identifier"""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model that uses email as the unique identifier instead of username"""
    
    username = None  # Remove username field
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email & Password are required by default
    
    objects = UserManager()
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extended profile information for users"""
    
    EDUCATION_CHOICES = [
        ('high_school', 'High School'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email}'s Profile"


class SavedScholarship(models.Model):
    """Model to store scholarships saved by users"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_scholarships')
    scholarship = models.ForeignKey('scholarships.Scholarship', on_delete=models.CASCADE)
    date_saved = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'scholarship')
        
    def __str__(self):
        return f"{self.user.email} - {self.scholarship.title}"


class ScholarshipApplication(models.Model):
    """Model to track scholarship applications by users"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    scholarship = models.ForeignKey('scholarships.Scholarship', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_applied = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.scholarship.title} ({self.status})"


class EmailVerification(models.Model):
    """Model to store email verification OTP codes"""
    
    VERIFICATION_TYPE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
    ]
    
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    verification_type = models.CharField(
        max_length=20, 
        choices=VERIFICATION_TYPE_CHOICES, 
        default='email_verification'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.email} - {self.otp_code}"
    
    def is_expired(self):
        """Check if OTP is expired (10 minutes)"""
        from django.conf import settings
        expire_time = self.created_at + timedelta(minutes=getattr(settings, 'OTP_EXPIRE_MINUTES', 10))
        return timezone.now() > expire_time
    
    def is_valid(self):
        """Check if OTP is valid (not used, not expired, not verified)"""
        return not self.is_used and not self.is_expired() and not self.is_verified
    
    @classmethod
    def generate_otp(cls, email, verification_type='email_verification'):
        """Generate a new OTP for the given email and verification type"""
        from django.conf import settings
        
        # Mark any existing OTPs of the same type as used
        cls.objects.filter(
            email=email, 
            verification_type=verification_type, 
            is_used=False
        ).update(is_used=True)
        
        # Generate new OTP
        otp_length = getattr(settings, 'OTP_LENGTH', 6)
        otp_code = ''.join(random.choices(string.digits, k=otp_length))
        
        return cls.objects.create(
            email=email, 
            otp_code=otp_code, 
            verification_type=verification_type
        )
