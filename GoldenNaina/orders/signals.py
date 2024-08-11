# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def update_stock(sender, instance, **kwargs):
    if instance.order_status in [Order.ORDER_CONFIRM, Order.ORDER_PROCESSED]:
        instance.decrease_stock()
