"""
URL configuration for scholarships_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from scholarships.views import ScholarshipViewSet
from scholarships_api.free_ai_views import FreeAIAssistantViewSet

router = DefaultRouter()
router.register(r'scholarships', ScholarshipViewSet)
router.register(r'ai', FreeAIAssistantViewSet, basename='free-ai-assistant')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/user/', include('users.urls')),  # Include user management URLs
    path('api/support/', include('ScholarshipSupport.urls')),  # Support/Contact endpoints
    path('api/livechat/', include('livechat.urls')),  # Live chat endpoints
    
    # Note: Removed django-allauth URLs due to Python 3.13 compatibility issues
    # Using custom Google OAuth implementation instead
]

# Add media URL configuration for profile pictures and other uploads
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
