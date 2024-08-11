from django.contrib import admin
from .models import Order, OrderedItem, Payment, Coupon, Cart_Offers


def approve_return(modeladmin, request, queryset):
    queryset.update(return_status=Order.RETURN_APPROVED)

def decline_return(modeladmin, request, queryset):
    queryset.update(return_status=Order.RETURN_DECLINED)
class OrderAdmin(admin.ModelAdmin):
    list_filter = [
        'owner',
        'order_status',
        'created_at',
        'updated_at',
    ]
    search_fields = (
        "owner",
        "order_status",
        "id",
    )

    actions =[approve_return, decline_return]
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'razorpay_payment_id', 'payment_method', 'amount', 'status', 'created_at')
    
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_price_display', 'owner', 'quantity', 'size', 'is_returned','return_request_date','return_approved_date')
    readonly_fields = ('product_price_display','quantity')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'discount', 'active')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedItem, OrderedItemAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Cart_Offers)