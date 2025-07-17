# scheduling_sessions/templatetags/scheduling_filters.py
from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def timesince_seconds(value, arg):
    """
    Calculates the difference in seconds between two datetime objects.
    Usage: {{ end_time|timesince_seconds:start_time }}
    """
    if not isinstance(value, timezone.datetime) or not isinstance(arg, timezone.datetime):
        return 0 # Or raise an error, depending on desired behavior

    # Ensure both are timezone-aware if USE_TZ is True
    if timezone.is_aware(value) and timezone.is_aware(arg):
        delta = value - arg
    elif timezone.is_naive(value) and timezone.is_naive(arg):
        delta = value - arg
    else:
        # Handle mixed aware/naive datetimes (convert to common timezone or raise error)
        # For simplicity, if mixed, return 0 or convert one to match the other's awareness
        return 0 # Or convert to UTC for comparison: value.astimezone(timezone.utc) - arg.astimezone(timezone.utc)

    return int(delta.total_seconds())

@register.filter
def divisibleby(value, arg):
    """
    Returns True if value is divisible by arg, False otherwise.
    """
    try:
        return int(value) % int(arg) == 0
    except (ValueError, ZeroDivisionError):
        return False

@register.filter
def floordiv(value, arg):
    """
    Performs floor division (integer division) of value by arg.
    """
    try:
        return int(value) // int(arg)
    except (ValueError, ZeroDivisionError):
        return 0 # Or handle as appropriate

@register.filter
def mod(value, arg):
    """
    Performs the modulo operation (remainder) of value by arg.
    """
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return 0 # Or handle as appropriate
