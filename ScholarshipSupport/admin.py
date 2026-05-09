from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'created_at']
    list_filter = ['status', 'subject', 'subscribe_newsletter', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'subscribe_newsletter')
        }),
        ('Admin', {
            'fields': ('status', 'assigned_to', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Name'
