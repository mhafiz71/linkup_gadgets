from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):
    """
    Send email notification when order status changes
    """
    if not created and instance.user and instance.user.email:
        # Only send email for status changes, not new orders
        if instance.status in ['paid', 'processing', 'shipped', 'delivered', 'cancelled']:
            subject = f'Order #{str(instance.id)[:8]} Status Update'
            
            # Render email template
            html_message = render_to_string('emails/order_status_update.html', {
                'order': instance,
                'user': instance.user,
            })
            
            try:
                send_mail(
                    subject=subject,
                    message=f'Your order status has been updated to: {instance.get_status_display()}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't break the order process
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to send order status email: {e}")