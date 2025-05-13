# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Consultation
from django.core.mail import send_mail

@receiver(post_save, sender=Consultation)
def send_approval_notification(sender, instance, created, **kwargs):
    if instance.status == 'accepted' and not instance.is_client_notified:
        # Send email notification
        send_mail(
            'Consultation Request Accepted',
            f'Hello {instance.client.first_name}, your consultation request with {instance.lawyer} has been accepted. You can now proceed to start the session.',
            'noreply@legalconsult.com',
            [instance.client.email],
            fail_silently=False,
        )

        # Mark the client as notified
        instance.is_client_notified = True
        instance.save()
