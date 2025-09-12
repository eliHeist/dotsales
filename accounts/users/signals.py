from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import CustomPasswordResetForm

from .models import User

@receiver(post_save, sender=User)
def send_password_setup_email(sender, instance, created, **kwargs):
    if created and instance.email:
        try:
            form = CustomPasswordResetForm({'email': instance.email})
            if form.is_valid():
                form.save(
                    request=None,  # Optional: pass real request if available
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    custom_message='Welcome to Tereka Online! Click below to set your password.',
                    reset_type="setup"
                )
        except Exception as e:
            print(f"\n\nERRORS:")
            print(e)
            print(f"Error sending password setup email: {e}")
