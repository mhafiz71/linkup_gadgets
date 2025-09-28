from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def currency(value):
    """Format a number as currency with 2 decimal places"""
    if value is None:
        return "0.00"
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return "0.00"

@register.filter
def format_order_id(order_id):
    """Format order ID to show first 8 characters"""
    return str(order_id)[:8]