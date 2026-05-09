from rest_framework import serializers
from .models import ChatRoom, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    sender_user_name = serializers.CharField(source='sender_user.get_full_name', read_only=True)
    sender_user_email = serializers.CharField(source='sender_user.email', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'chat_room',
            'sender',
            'sender_user',
            'sender_user_name',
            'sender_user_email',
            'message',
            'is_read',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'sender_user', 'sender_user_name', 'sender_user_email']


class ChatRoomSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    support_agent_name = serializers.CharField(source='support_agent.get_full_name', read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'id',
            'user',
            'user_name',
            'user_email',
            'support_agent',
            'support_agent_name',
            'is_active',
            'messages',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user', 'user_name', 'user_email', 'support_agent_name']
