from django.contrib import admin
from .models import ChatRoom, ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'support_agent', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'support_agent__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Chat Information', {
            'fields': ('user', 'support_agent', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'sender_user', 'is_read', 'created_at')
    list_filter = ('sender', 'is_read', 'created_at')
    search_fields = ('message', 'sender_user__email')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Message Information', {
            'fields': ('chat_room', 'sender', 'sender_user', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
