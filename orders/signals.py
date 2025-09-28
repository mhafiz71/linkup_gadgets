from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    """
    Send email notification when order status changes
    """
    if not created and instance.user and instance.user.email:
        # Only send email for meaningful status changes, not new orders
        if instance.status in ['processing', 'shipped', 'delivered', 'cancelled']:
            subject = f'Order #{str(instance.id)[:8]} Status Update - {instance.get_status_display()}'
            
            from core.email_utils import send_order_status_email
            send_order_status_email(instance)