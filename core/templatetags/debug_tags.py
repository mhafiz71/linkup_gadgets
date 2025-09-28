from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def debug_info():
    """Return debug information for troubleshooting"""
    return {
        'debug': settings.DEBUG,
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'media_url': settings.MEDIA_URL,
    }

@register.simple_tag(takes_context=True)
def csrf_debug(context):
    """Debug CSRF token information"""
    request = context.get('request')
    if request:
        return {
            'csrf_token': request.META.get('CSRF_COOKIE'),
            'secure': request.is_secure(),
            'host': request.get_host(),
        }
    return {}