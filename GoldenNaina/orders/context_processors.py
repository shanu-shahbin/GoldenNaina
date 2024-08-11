from .models import Order

def cart_item_count(request):
    if request.user.is_authenticated:
        customer = request.user.customer_profile
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        return {'cart_item_count': cart_obj.added_items.count()}
    return {'cart_item_count': 0}
