from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the given value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def order_status_class(status):
    status_classes = {
        "Processing": "Processing",
        "Confirmed": "Confirmed",
        "Out for Delivery": "Out",
        "Cancelled": "Cancelled",
    }
    return status_classes.get(status, "Pending")