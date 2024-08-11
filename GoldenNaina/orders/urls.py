from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from paypal.standard.ipn import urls as paypal_urls

urlpatterns =[
    # cart

    path('cart', views.show_cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:pk>', views.remove_item_from_cart, name='remove_item'),

    path('checkout', views.checkout_process, name='checkout'),
    
    path('coupons', views.Coupons_view, name='coupons'),
    
    # payment

    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/<int:address_id>/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),

    # orders

    path('orders/', views.show_orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # returns and refunds

    path('orders/return/<int:order_id>/', views.request_return, name='return_order'),
    path('orders/refund/<int:order_id>/', views.request_refund, name='request_refund'),
    path('refund_approved/', views.refund_approved, name='refund_approved'),

]