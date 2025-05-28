from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.shortcuts import render
import json
import requests
from django.conf import settings

User = get_user_model()


def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def verify_google_id_token(id_token):
    """Verify a Google ID token and return user info"""
    try:
        # Verify the token using Google's tokeninfo endpoint
        response = requests.get(
            'https://oauth2.googleapis.com/tokeninfo',
            params={'id_token': id_token}
        )
        
        if response.status_code != 200:
            return None
            
        user_info = response.json()
        
        # Verify the token's audience matches our client ID
        if user_info.get('aud') != settings.GOOGLE_CLIENT_ID:
            print("Token audience mismatch")
            return None
        
        return {
            'email': user_info.get('email'),
            'email_verified': user_info.get('email_verified', False),
            'name': user_info.get('name'),
            'picture': user_info.get('picture'),
            'given_name': user_info.get('given_name'),
            'family_name': user_info.get('family_name'),
        }
    except Exception as e:
        print(f"Error verifying Google token: {e}")
        return None


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(View):
    """Process Google login redirects and generate JWT tokens"""
    
    def get(self, request):
        """Redirect URL after Google authentication"""
        # For demo purposes, we'll simulate getting a code from Google
        code = request.GET.get('code', 'demo-auth-code')
        
        # In production, this would be an actual OAuth flow
        # But for development, we'll use a simplified approach
        try:
            # Simulate user data for demo purposes
            # In production, you'd exchange the code for tokens using Google API
            email = request.GET.get('email', 'demo@example.com')
            name = request.GET.get('name', 'Demo User')
            
            # Create or get the user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': name,
                    'is_active': True,
                }
            )
            
            # Generate tokens for the user
            tokens = get_tokens_for_user(user)
            
            # Render the callback template that will communicate with frontend
            return render(request, 'oauth_callback.html', {
                'token': tokens['access'],
                'user_id': user.id,
                'email': user.email,
                'name': user.full_name or '',
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth_token(request):
    """Exchange Google ID token for our JWT token"""
    id_token = request.data.get('id_token')
    if not id_token:
        return JsonResponse({'error': 'Google ID token is required'}, status=400)
    
    # Verify the token with Google
    user_info = verify_google_id_token(id_token)
    
    if not user_info:
        return JsonResponse({'error': 'Invalid Google ID token'}, status=400)
    
    try:
        # Extract user info from the verified token
        email = user_info.get('email')
        
        if not email:
            return JsonResponse({'error': 'Email not provided in the ID token'}, status=400)
        
        # Check if the email is verified (Google should verify emails)
        if not user_info.get('email_verified'):
            return JsonResponse({'error': 'Email not verified by Google'}, status=400)
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'full_name': user_info.get('name', ''),
                'is_active': True,
            }
        )
        
        # If user exists but doesn't have a name, update it
        if not created and not user.full_name and user_info.get('name'):
            user.full_name = user_info.get('name')
            user.save(update_fields=['full_name'])
        
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)
        
        # Include user data in response
        response_data = {
            'token': tokens['access'],
            'refresh': tokens['refresh'],
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
            }
        }
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def social_auth_success(request):
    """Success page after social auth"""
    return JsonResponse({
        'message': 'Social authentication successful. You can close this window.'
    })
