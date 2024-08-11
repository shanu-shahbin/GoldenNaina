from django import template

register = template.Library()

@register.simple_tag()
def get_return_status(return_status):
    from orders.models import Order
    return_status_array = {
        'requested': 'Return Requested',
        'approved': 'Return Approved',
        'declined': 'Return Declined',
        'Refund Initiated': 'Refund Initiated',
        'Refund completed': 'Refund Completed'

    }
    return return_status_array.get(return_status, 'No Return Status')
