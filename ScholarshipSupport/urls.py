from django.urls import path
from .views import (
    ContactMessageCreateView,
    ContactMessageListView,
    ContactMessageDetailView
)

urlpatterns = [
    # Public endpoint - submit contact form
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    
    # Admin endpoints - manage messages
    path('contact/messages/', ContactMessageListView.as_view(), name='contact-list'),
    path('contact/messages/<int:pk>/', ContactMessageDetailView.as_view(), name='contact-detail'),
]
