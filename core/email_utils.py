"""
Email utility functions for LinkUp Gadgets
"""
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)

def send_template_email(subject, template_name, context, recipient_list, fail_silently=True):
    """
    Send an email using a template with proper error handling and logging
    
    Args:
        subject (str): Email subject
        template_name (str): Path to HTML template
        context (dict): Template context variables
        recipient_list (list): List of recipient email addresses
        fail_silently (bool): Whether to suppress email errors
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Render HTML and plain text versions
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently,
        )
        
        logger.info(f"Email sent successfully: '{subject}' to {recipient_list}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email '{subject}' to {recipient_list}: {e}")
        if not fail_silently:
            raise
        return False

def send_welcome_email(user, is_vendor=False):
    """Send welcome email to new user"""
    subject = f"Welcome to LinkUp Gadgets - Your {'Vendor ' if is_vendor else ''}Account is Ready!"
    return send_template_email(
        subject=subject,
        template_name='emails/welcome_email.html',
        context={'user': user, 'is_vendor': is_vendor},
        recipient_list=[user.email]
    )

def send_order_confirmation_email(order):
    """Send order confirmation email"""
    subject = f'Your LinkUp Gadgets Order Confirmation (#{str(order.id)[:8]})'
    
    # Send to both order email and user email if different
    recipient_list = [order.email]
    if order.user and order.user.email and order.user.email != order.email:
        recipient_list.append(order.user.email)
    
    return send_template_email(
        subject=subject,
        template_name='emails/order_confirmation_email.html',
        context={'order': order},
        recipient_list=recipient_list,
        fail_silently=False  # Don't fail silently for order confirmations
    )

def send_order_status_email(order):
    """Send order status update email"""
    subject = f'Order #{str(order.id)[:8]} Status Update - {order.get_status_display()}'
    
    # Send to both order email and user email if different
    recipient_list = [order.user.email]
    if order.email and order.email != order.user.email:
        recipient_list.append(order.email)
    
    return send_template_email(
        subject=subject,
        template_name='emails/order_status_update.html',
        context={'order': order, 'user': order.user},
        recipient_list=recipient_list,
        fail_silently=False  # Don't fail silently for order updates
    )