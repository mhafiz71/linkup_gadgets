"""
Management command to test email functionality
Usage: python manage.py test_emails
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from core.email_utils import send_welcome_email, send_template_email
from orders.models import Order

class Command(BaseCommand):
    help = 'Test email functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address to send test emails to',
            default='test@example.com'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write(f"Testing email functionality...")
        self.stdout.write(f"Email Backend: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"Email Host: {settings.EMAIL_HOST}")
        self.stdout.write(f"Default From Email: {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"Test Email: {test_email}")
        
        # Test 1: Simple email
        self.stdout.write("\n1. Testing simple email...")
        success = send_template_email(
            subject="LinkUp Gadgets - Email Test",
            template_name='emails/welcome_email.html',
            context={
                'user': {'first_name': 'Test', 'username': 'testuser'},
                'is_vendor': False
            },
            recipient_list=[test_email]
        )
        
        if success:
            self.stdout.write(self.style.SUCCESS("✓ Simple email test passed"))
        else:
            self.stdout.write(self.style.ERROR("✗ Simple email test failed"))
        
        # Test 2: Welcome email with real user (if exists)
        self.stdout.write("\n2. Testing welcome email...")
        try:
            user = User.objects.first()
            if user:
                success = send_welcome_email(user, is_vendor=False)
                if success:
                    self.stdout.write(self.style.SUCCESS("✓ Welcome email test passed"))
                else:
                    self.stdout.write(self.style.ERROR("✗ Welcome email test failed"))
            else:
                self.stdout.write(self.style.WARNING("⚠ No users found to test welcome email"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Welcome email test error: {e}"))
        
        # Test 3: Order confirmation (if orders exist)
        self.stdout.write("\n3. Testing order confirmation email...")
        try:
            order = Order.objects.first()
            if order:
                from core.email_utils import send_order_confirmation_email
                success = send_order_confirmation_email(order)
                if success:
                    self.stdout.write(self.style.SUCCESS("✓ Order confirmation email test passed"))
                else:
                    self.stdout.write(self.style.ERROR("✗ Order confirmation email test failed"))
            else:
                self.stdout.write(self.style.WARNING("⚠ No orders found to test order confirmation email"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Order confirmation email test error: {e}"))
        
        self.stdout.write(f"\nEmail testing completed!")
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            self.stdout.write(self.style.WARNING(
                "\nNote: You're using console email backend. "
                "Emails will be printed to console instead of being sent."
            ))
        
        self.stdout.write(f"\nTo configure real email sending, update your .env file with:")
        self.stdout.write("EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
        self.stdout.write("EMAIL_HOST=smtp.gmail.com")
        self.stdout.write("EMAIL_PORT=587")
        self.stdout.write("EMAIL_USE_TLS=True")
        self.stdout.write("EMAIL_HOST_USER=your-email@gmail.com")
        self.stdout.write("EMAIL_HOST_PASSWORD=your-app-password")
        self.stdout.write("DEFAULT_FROM_EMAIL=LinkUp Gadgets <your-email@gmail.com>")