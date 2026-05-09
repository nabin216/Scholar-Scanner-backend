from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for creating contact messages from the frontend"""
    
    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'subject',
            'message',
            'subscribe_newsletter',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_email(self, value):
        """Validate email format"""
        return value.lower().strip()
    
    def validate_first_name(self, value):
        """Clean first name"""
        return value.strip().title()
    
    def validate_last_name(self, value):
        """Clean last name"""
        return value.strip().title()


class ContactMessageAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin to view/manage contact messages"""
    full_name = serializers.ReadOnlyField()
    subject_display = serializers.CharField(source='get_subject_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = '__all__'
