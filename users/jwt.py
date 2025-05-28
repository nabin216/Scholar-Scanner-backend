from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes user data in the response
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['full_name'] = user.full_name
        token['is_staff'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra responses
        user = self.user
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'is_staff': user.is_staff,
        }
        
        # Add profile data if exists
        try:
            if hasattr(user, 'profile'):
                data['user']['profile'] = {
                    'bio': user.profile.bio,
                    'education': user.profile.education,
                }
        except:
            pass
            
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use our enhanced token serializer
    """
    serializer_class = CustomTokenObtainPairSerializer
