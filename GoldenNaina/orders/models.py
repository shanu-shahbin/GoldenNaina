from django.db import models
from Customers.models import Customer, Customer_Address
from products.models import Product, ProductImages, Stock, Size
from django.contrib import admin  
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta


class Order(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))
    CART_STAGE = 0
    ORDER_CONFIRM = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    ORDER_CANCELLED = 5
    STATUS_CHOICES = (
        (ORDER_CONFIRM, 'ORDER_CONFIRM'),
        (ORDER_PROCESSED, 'ORDER_PROCESSED'),
        (ORDER_DELIVERED, "ORDER_DELIVERED"),
        (ORDER_CANCELLED, "ORDER_CANCELLED")
    )
    RETURN_REQUESTED = 'requested'
    RETURN_APPROVED = 'approved'
    RETURN_DECLINED = 'declined'
    REFUND_INITIATED = 'Refund Initiated'
    REFUND_COMPLETED = 'Refund completed'
    RETURN_STATUS_CHOICES = [
        (RETURN_REQUESTED, 'Return Requested'),
        (RETURN_APPROVED, 'Return Approved'),
        (RETURN_DECLINED, 'Return Declined'),
        (REFUND_INITIATED, 'Refund Initiated'),
        (REFUND_COMPLETED , 'Refund completed'),
    ]
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=CART_STAGE)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupons = models.ManyToManyField('Coupon', blank=True)
    total_price = models.FloatField(default=0.00)
    address = models.ForeignKey(Customer_Address, on_delete=models.SET_NULL, null=True, related_name='orders')
    return_status = models.CharField(
        max_length=20,
        choices=RETURN_STATUS_CHOICES,
        default=None,
        blank=True,
        null=True
    )
    is_refund_requested = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    is_refund_paid = models.BooleanField(default=False)
    return_reason = models.TextField(null=True, blank=True)
    return_request_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    ifsc_code = models.CharField(max_length=255, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=[('paypal', 'PayPal'), ('cod', 'Cash on Delivery')], default='paypal')

    def cancel_order(self):
        self.order_status = self.ORDER_CANCELLED
        self.save()

    def decrease_stock(self):
        for item in self.added_items.all():
            try:
                size_obj = Size.objects.get(name=item.size)
                print(f"Trying to decrease stock for Product: {item.product}, Size: {size_obj.name}, Quantity: {item.quantity}")
                
                stock_item = Stock.objects.get(product=item.product, size=size_obj)
                print(f"Current stock quantity for Product: {item.product}, Size: {size_obj.name} is {stock_item.quantity}")
                
                stock_item.quantity -= item.quantity
                stock_item.save()

                print(f"Stock decreased for Product: {item.product}, Size: {size_obj.name}, New Quantity: {stock_item.quantity}")
                
            except Size.DoesNotExist:
                print(f"Size {item.size} does not exist")
            except Stock.DoesNotExist:
                print(f"Stock item does not exist for Product: {item.product}, Size: {item.size}")
            except Exception as e:
                print(f"Error updating stock: {e}")

    def is_within_return_period(self):
        for item in self.added_items.all():
            return_policy_days = item.get_return_policy_days()
            if (timezone.now() - self.created_at) > timedelta(days=return_policy_days):
                return False
        return True




class OrderedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='added_items')
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=5, choices=[('L', 'Large'), ('M', 'Medium'), ('S', 'Small'), ('XXL', 'Extra Extra Large'), ('XL', 'Extra Large')], null=True) 
    is_returned = models.BooleanField(default=False)
    return_request_date = models.DateTimeField(null=True, blank=True)
    return_approved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.title} ( {self.size} ) x {self.quantity}"

    @property
    def product_price(self):
        return self.product.discount_price if self.product else 'No product'

    @admin.display(description='Product Price')
    def product_price_display(self):
        return self.product_price

    def get_return_policy_days(self):
        # Fetch the return policy days from the associated product
        return int(self.product.return_policy)

    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField(help_text='Percentage discount')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
    description = models.TextField(blank=True, help_text='Description of the coupon')
    terms_and_conditions = models.TextField(blank=True, help_text='Terms and conditions of the coupon', null=True)

    def __str__(self):
        return self.code

class Cart_Offers(models.Model):
    offer_id = models.CharField(max_length=100)
    offer_name = models.CharField(max_length=200)
    offer_description = models.TextField()

    def __str__(self):
        return self.offer_name

class Payment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=20, choices=[('paypal', 'PayPal'), ('cod', 'Cash on Delivery')], default='paypal')
    paid = models.BooleanField(default=False)
    amount = models.FloatField(default=0.00)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.name} - {self.order.id}"