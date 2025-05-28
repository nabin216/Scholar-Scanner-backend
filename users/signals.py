from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for newly created User instances"""
    if created:
        UserProfile.objects.get_or_create(user=instance)

# Note: We've removed the SocialAccount signal handler as we're not using allauth's
# social account functionality directly due to cryptography package issues
