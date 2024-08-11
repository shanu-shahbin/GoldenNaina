from django import template
from datetime import timedelta

register = template.Library()

@register.simple_tag(name='getstatus')
def getstatus(status):
    status = status - 1
    status_array = ["Processing", "Shipped", "Delivered", "Cancelled", "Cancelled"]
    return status_array[status]

@register.simple_tag(name='getstatus_time')
def getstatus_time(order, status):
    status_timestamps = {
        order.ORDER_CONFIRM: order.created_at,
        order.ORDER_PROCESSED: order.created_at + timedelta(days=1),  # Example, adjust as needed
        order.ORDER_DELIVERED: order.created_at + timedelta(days=5),  # Example, adjust as needed
        order.ORDER_CANCELLED: order.updated_at if order.order_status == order.ORDER_CANCELLED else None
    }
    return status_timestamps.get(status, "Not Available")
