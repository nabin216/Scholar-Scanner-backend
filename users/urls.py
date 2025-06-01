from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views
from .jwt import CustomTokenObtainPairView
from .social_auth import GoogleLoginView, google_auth_token, social_auth_success

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'saved-scholarships', views.SavedScholarshipViewSet, basename='saved-scholarship')
router.register(r'applications', views.ScholarshipApplicationViewSet, basename='application')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
      # Standard Authentication endpoints
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/me/', views.UserViewSet.as_view({'get': 'me'}), name='me'),
    path('auth/change-password/', views.UserViewSet.as_view({'post': 'change_password'}), name='change-password'),
    
    # Email Verification endpoints
    path('auth/send-verification-email/', views.send_verification_email, name='send_verification_email'),
    path('auth/verify-otp/', views.verify_otp, name='verify_otp'),
    path('auth/resend-otp/', views.resend_otp, name='resend_otp'),
    
    # Social Authentication endpoints
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/google/token/', google_auth_token, name='google_auth_token'),
    path('social-auth-success/', social_auth_success, name='social_auth_success'),
]
