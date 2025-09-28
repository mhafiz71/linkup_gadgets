# Email Configuration Guide for LinkUp Gadgets

## 📧 Email Types Implemented

### 1. Welcome Emails
- **Trigger**: User registration (both customers and vendors)
- **Template**: `templates/emails/welcome_email.html`
- **Function**: `core.email_utils.send_welcome_email()`
- **Features**: 
  - Different content for vendors vs customers
  - Professional HTML design with branding
  - Call-to-action button

### 2. Order Confirmation Emails
- **Trigger**: Successful payment completion
- **Template**: `templates/emails/order_confirmation_email.html`
- **Function**: `core.email_utils.send_order_confirmation_email()`
- **Features**:
  - Order details and itemized list
  - Payment confirmation
  - Order tracking information

### 3. Order Status Update Emails
- **Trigger**: Order status changes (processing, shipped, delivered, cancelled)
- **Template**: `templates/emails/order_status_update.html`
- **Function**: `core.email_utils.send_order_status_email()`
- **Features**:
  - Status-specific messaging
  - Order tracking information
  - Professional design

## ⚙️ Email Configuration

### Current Settings (Development)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Prints to console
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = 'webmaster@localhost'
```

### Production Settings (Gmail SMTP)
Create a `.env` file with:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=LinkUp Gadgets <your-email@gmail.com>
```

### Alternative SMTP Providers

#### SendGrid
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=LinkUp Gadgets <noreply@linkupgadgets.com>
```

#### Mailgun
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=postmaster@your-domain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
DEFAULT_FROM_EMAIL=LinkUp Gadgets <noreply@linkupgadgets.com>
```

## 🧪 Testing Email Functionality

### Test Command
```bash
python manage.py test_emails --email your-test@email.com
```

### Manual Testing
```python
# In Django shell (python manage.py shell)
from core.email_utils import send_welcome_email
from django.contrib.auth.models import User

user = User.objects.first()
send_welcome_email(user, is_vendor=False)
```

## 🔧 Email Utility Functions

### `send_template_email()`
Generic function for sending templated emails with error handling and logging.

### `send_welcome_email(user, is_vendor=False)`
Sends welcome email to new users with different content for vendors.

### `send_order_confirmation_email(order)`
Sends order confirmation after successful payment.

### `send_order_status_email(order)`
Sends status update emails when order status changes.

## 📝 Email Templates

All email templates use responsive HTML design with:
- LinkUp Gadgets branding
- Professional styling
- Mobile-friendly layout
- Consistent color scheme (#1E2A47, #FBBF24)

### Template Structure
```
templates/emails/
├── welcome_email.html          # Welcome email for new users
├── order_confirmation_email.html  # Order confirmation
└── order_status_update.html    # Status updates
```

## 🚨 Error Handling

- All email functions include comprehensive error handling
- Errors are logged but don't break the user flow
- Failed emails are logged with details for debugging
- Option to fail silently or raise exceptions

## 📊 Email Logging

Email sending is logged with:
- Success/failure status
- Recipient information
- Error details (if any)
- Timestamps

Check logs in `logs/django.log` for email-related entries.

## 🔒 Security Considerations

1. **App Passwords**: Use app-specific passwords for Gmail
2. **Environment Variables**: Never commit email credentials to version control
3. **TLS/SSL**: Always use encrypted connections for production
4. **Rate Limiting**: Consider email rate limits for high-volume sending

## 📈 Production Recommendations

1. **Use Professional Email Service**: SendGrid, Mailgun, or AWS SES
2. **Domain Authentication**: Set up SPF, DKIM, and DMARC records
3. **Monitoring**: Monitor email delivery rates and bounces
4. **Templates**: Consider using email service templates for better deliverability
5. **Unsubscribe**: Add unsubscribe links for marketing emails

## 🐛 Troubleshooting

### Common Issues

1. **Emails not sending**
   - Check EMAIL_BACKEND setting
   - Verify SMTP credentials
   - Check firewall/network restrictions

2. **Emails going to spam**
   - Set up domain authentication
   - Use professional from address
   - Avoid spam trigger words

3. **Template errors**
   - Check template syntax
   - Verify context variables
   - Test with simple templates first

### Debug Commands
```bash
# Test email configuration
python manage.py test_emails

# Check email backend
python manage.py shell
>>> from django.conf import settings
>>> print(settings.EMAIL_BACKEND)

# Send test email
python manage.py sendtestemail your-email@example.com
```

## 📞 Support

For email configuration issues:
1. Check Django email documentation
2. Verify SMTP provider settings
3. Test with simple email first
4. Check server logs for errors