
from .models import Customer_Address

def customer_addresses(request):
    if request.user.is_authenticated:
        customer_profile = getattr(request.user, 'customer_profile', None)
        if customer_profile:
            addresses = Customer_Address.objects.filter(customer=customer_profile)
            return {'customer_addresses': addresses}
    return {'customer_addresses': []}
