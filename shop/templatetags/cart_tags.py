"""Custom template tags for the shop application."""

from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply a value by an argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    """Format a value as GBP currency."""
    try:
        return f'£{float(value):.2f}'
    except (ValueError, TypeError):
        return '£0.00'
