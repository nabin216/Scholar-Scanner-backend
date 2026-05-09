from django.db import models
from django.conf import settings


class ContactMessage(models.Model):
    """Model to store contact form submissions from Get in Touch page"""
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('partnership', 'Partnership Opportunity'),
        ('media', 'Media Inquiry'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Sender Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    
    # Message Details
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    
    # Newsletter Subscription
    subscribe_newsletter = models.BooleanField(default=False)
    
    # Admin/Status fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_messages'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_subject_display()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
