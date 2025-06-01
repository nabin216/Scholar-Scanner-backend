from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import UserProfile, SavedScholarship, ScholarshipApplication, EmailVerification
from .serializers import (
    UserSerializer, UserRegistrationSerializer, ChangePasswordSerializer,
    SavedScholarshipSerializer, ScholarshipApplicationSerializer, UserProfileSerializer,
    EmailVerificationSerializer, OTPVerificationSerializer
)
from .permissions import IsOwnerOrReadOnly
from .email_service import send_verification_email as send_email_with_otp, send_welcome_email

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
def send_verification_email(request):
    """Send OTP verification email"""
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'This email is already registered. Please try logging in instead.'},
                status=status.HTTP_400_BAD_REQUEST
            )        # Generate and send OTP
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
def resend_otp(request):
    """Resend OTP verification email"""
    serializer = EmailVerificationSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        
        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'This email is already registered.'},
                status=status.HTTP_400_BAD_REQUEST
            )        # Generate new OTP
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
