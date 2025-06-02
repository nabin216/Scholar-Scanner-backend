from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import logging
from .throttling import RegistrationRateThrottle, EmailVerificationRateThrottle

# Set up logging
logger = logging.getLogger(__name__)

from .models import UserProfile, SavedScholarship, ScholarshipApplication, EmailVerification
from .serializers import (
    UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer,
    SavedScholarshipSerializer, ScholarshipApplicationSerializer, UserProfileSerializer,
    EmailVerificationSerializer, OTPVerificationSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from .permissions import IsOwnerOrReadOnly
from .email_service import send_verification_email as send_email_with_otp, send_welcome_email, send_password_reset_otp

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users"""
    
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()
    
    def get_queryset(self):
        # Regular users can only see their own profile
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.all()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], url_path='update-profile')
    def update_profile(self, request):
        """Update current user's profile"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """Change current user's password"""
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check old password
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({"message": "Password updated successfully"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration with email verification"""
    
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    throttle_classes = [RegistrationRateThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send welcome email
        send_welcome_email(user)
        
        # Generate JWT tokens for the new user
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Registration successful! Your email has been verified.',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationRateThrottle])
def send_verification_email(request):
    """Send OTP verification email with rate limiting"""
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'This email is already registered. Please try logging in instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check for recent OTPs for this email that might still be valid
            recent_otp = EmailVerification.objects.filter(
                email=email,
                is_used=False,
                created_at__gte=timezone.now() - timedelta(minutes=9)  # Just under the 10-minute expiry
            ).first()
            
            if recent_otp:
                time_elapsed = timezone.now() - recent_otp.created_at
                time_elapsed_seconds = time_elapsed.total_seconds()
                remaining_seconds = 60 - time_elapsed_seconds
                
                # If OTP was generated less than 60 seconds ago, tell user to wait
                if remaining_seconds > 0:
                    return Response({
                        'message': f'A verification code was already sent to {email}. Please wait {int(remaining_seconds)} seconds before requesting another code.',
                        'canResend': False,
                        'waitTime': int(remaining_seconds)
                    }, status=status.HTTP_200_OK)
                
                # If OTP is between 60 seconds and 9 minutes old, suggest using existing code
                return Response({
                    'message': f'A verification code was already sent to {email}. Please check your inbox or spam folder.',
                    'canResend': True,
                    'email': email
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error(f"Error checking recent OTPs: {e}")
        
        # Generate and send OTP
        otp_obj = EmailVerification.generate_otp(email)
        
        if send_email_with_otp(email, otp_obj.otp_code):
            return Response({
                'message': f'Verification code sent to {email}. Please check your email.',
                'email': email
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to send verification email. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    """Verify OTP code"""
    serializer = OTPVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        
        try:
            otp_obj = EmailVerification.objects.filter(
                email=email,
                otp_code=otp_code,
                is_used=False,
                is_verified=False
            ).latest('created_at')
            
            if otp_obj.is_valid():
                return Response({
                    'message': 'OTP verified successfully. You can now complete your registration.',
                    'verified': True
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'OTP has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except EmailVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid OTP code.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationRateThrottle])
def resend_otp(request):
    """Resend OTP verification email with rate limiting"""
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'This email is already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check for very recent OTPs for this email to prevent hammering the endpoint
            recent_otp = EmailVerification.objects.filter(
                email=email,
                is_used=False,
                created_at__gte=timezone.now() - timedelta(seconds=30)  # Shorter window for resend
            ).first()
            
            if recent_otp:
                time_elapsed = timezone.now() - recent_otp.created_at
                time_elapsed_seconds = time_elapsed.total_seconds()
                remaining_seconds = 30 - time_elapsed_seconds
                
                if remaining_seconds > 0:
                    return Response({
                        'message': f'Please wait {int(remaining_seconds)} seconds before requesting another code.',
                        'waitTime': int(remaining_seconds)
                    }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        except Exception as e:
            logger.error(f"Error checking recent OTPs: {e}")
            
        # Generate new OTP
        otp_obj = EmailVerification.generate_otp(email)
        
        if send_email_with_otp(email, otp_obj.otp_code):
            return Response({
                'message': f'New verification code sent to {email}.',
                'email': email
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Failed to send verification email. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedScholarshipViewSet(viewsets.ModelViewSet):
    """API endpoint for saved scholarships"""
    
    serializer_class = SavedScholarshipSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SavedScholarship.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScholarshipApplicationViewSet(viewsets.ModelViewSet):
    """API endpoint for scholarship applications"""
    
    serializer_class = ScholarshipApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ScholarshipApplication.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([EmailVerificationRateThrottle])
def password_reset_request(request):
    """Request password reset by sending OTP to email"""
    serializer = PasswordResetRequestSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        try:
            # Generate OTP for password reset
            otp_obj = EmailVerification.generate_otp(email, 'password_reset')
            
            # Send password reset email
            email_sent = send_password_reset_otp(email, otp_obj.otp_code)
            
            if email_sent:
                return Response({
                    'message': 'Password reset code has been sent to your email address.',
                    'email': email
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Failed to send password reset email. Please try again.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except Exception as e:
            logger.error(f"Password reset request failed for {email}: {e}")
            return Response(
                {'error': 'An error occurred while processing your request.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirm password reset with OTP and set new password"""
    serializer = PasswordResetConfirmSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        new_password = serializer.validated_data['new_password']
        
        try:
            # Get the user
            user = User.objects.get(email=email)
            
            # Mark OTP as used
            otp_obj = EmailVerification.objects.filter(
                email=email,
                otp_code=otp_code,
                verification_type='password_reset',
                is_used=False
            ).latest('created_at')
            
            otp_obj.is_used = True
            otp_obj.is_verified = True
            otp_obj.save()
            
            # Update user password
            user.set_password(new_password)
            user.save()
            
            logger.info(f"Password reset successful for user: {email}")
            
            return Response({
                'message': 'Password has been reset successfully. You can now log in with your new password.'
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except EmailVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired OTP code.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Password reset confirmation failed for {email}: {e}")
            return Response(
                {'error': 'An error occurred while resetting your password.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
