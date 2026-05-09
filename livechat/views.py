from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Users see their own rooms, support agents see all rooms
        if user.is_staff:
            return ChatRoom.objects.all()
        return ChatRoom.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        # Create a new chat room for the current user
        chat_room, created = ChatRoom.objects.get_or_create(
            user=request.user,
            is_active=True
        )
        serializer = self.get_serializer(chat_room)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        chat_room = self.get_object()
        
        # Verify user has access to this chat room
        if chat_room.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have access to this chat room.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        message_text = request.data.get('message', '').strip()
        if not message_text:
            return Response(
                {'detail': 'Message cannot be empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Determine sender type
        sender_type = 'user' if chat_room.user == request.user else 'support'
        
        message = ChatMessage.objects.create(
            chat_room=chat_room,
            sender=sender_type,
            sender_user=request.user,
            message=message_text
        )
        
        serializer = ChatMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        chat_room = self.get_object()
        
        # Verify user has access to this chat room
        if chat_room.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have access to this chat room.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        messages = chat_room.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def close_chat(self, request, pk=None):
        chat_room = self.get_object()
        
        # Only the user or support agent can close the chat
        if chat_room.user != request.user and chat_room.support_agent != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to close this chat.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        chat_room.is_active = False
        chat_room.save()
        serializer = self.get_serializer(chat_room)
        return Response(serializer.data)


class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see messages from their chat rooms
        user = self.request.user
        if user.is_staff:
            return ChatMessage.objects.all()
        chat_rooms = ChatRoom.objects.filter(user=user)
        return ChatMessage.objects.filter(chat_room__in=chat_rooms)
