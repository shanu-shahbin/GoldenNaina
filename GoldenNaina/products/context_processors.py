from django.template import Context
from .models import Product, Category, Wishlist
from django.contrib import messages


def default(request):
    categories = Category.objects.all()
    wishlist = Wishlist.objects.all()
    wishlist_count = 0

    if request.user.is_authenticated:
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
        except Wishlist.DoesNotExist:
            messages.warning(request, 'You need to login to see your wishlist')
    
    return {
        'categories': categories,
        'products': Product.objects.all(),
        'wishlist_count': wishlist_count,
        'wishlist': wishlist,
    }