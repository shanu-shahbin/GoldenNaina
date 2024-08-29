from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import OrderedItem, Order, Coupon, Cart_Offers
from products.models import Product
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import uuid
from Customers.models import Customer_Address, Customer
from django.utils import timezone
from django.http import JsonResponse
import time
from django.core.exceptions import MultipleObjectsReturned
from products.models import Stock, Size

@login_required
def show_cart(request):
    cart_offers = Cart_Offers.objects.all()
    user = request.user
    customer = user.customer_profile
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )
    cart_item_count = cart_obj.added_items.count()

    # Fetch stock information for each cart item
    cart_items = cart_obj.added_items.all()
    for item in cart_items:
        try:
            # Assuming item.size is the name of the size, not the id
            size_obj = Size.objects.get(name=item.size)
            item.stock = Stock.objects.filter(product=item.product, size=size_obj).first()
        except Size.DoesNotExist:
            item.stock = None
            print(f"No Size matches the given query: {item.size}")

    context = {
        'cart': cart_obj,
        'cart_offers': cart_offers,
        'cart_item_count': cart_item_count,
        'addresses': customer.addresses.all(),
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)




@login_required
def remove_item_from_cart(request, pk):
    ordered_item = OrderedItem.objects.get(pk=pk)
    cart_obj = ordered_item.owner
    ordered_item.delete()
    if not cart_obj.added_items.exists():
        cart_obj.delete()
        return redirect('cart')
    return redirect('cart')

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = user.customer_profile
        quantity = int(request.POST.get('quantity'))
        size = request.POST.get('size')
        product_id = request.POST.get('product_id')
        
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        product = get_object_or_404(Product, pk=product_id)
        
        # Include size in the get_or_create to treat items with different sizes as distinct
        ordered_item, created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj,
            size=size,  # Include size here
            defaults={'quantity': quantity}
        )

        if not created:
            ordered_item.quantity += quantity
            ordered_item.save()
        else:
            ordered_item.quantity = quantity
            ordered_item.size = size
            ordered_item.save()

    return redirect('cart')


@login_required
def checkout_process(request):
    if request.method == "POST":
        total = request.POST.get('total')
        coupon_code = request.POST.get('code')
        user = request.user

        if total is None:
            print("Total is None. Make sure the form is correctly submitting the total value.")
            return redirect('cart')

        try:
            total = float(total)
        except ValueError as e:
            print(f"Invalid total value: {total}. Error: {e}")
            return redirect('cart')

        customer = user.customer_profile

        if not customer.addresses.exists():
            print("Customer has no address. Redirecting to add address.")
            return redirect('add_address')

        try:
            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )

            for item in order_obj.added_items.all():
                quantity = request.POST.get(f'quantity_{item.id}')
                size = request.POST.get(f'size_{item.id}')
                if quantity and size:
                    try:
                        item.quantity = int(quantity)
                        item.size = size
                        item.save()
                    except ValueError as e:
                        print(f"Invalid quantity value for item {item.id}: {quantity}. Error: {e}")
                        return redirect('cart')

            if 'apply_remove_coupon' in request.POST:
                discount = 0.0

                if coupon_code and 'Remove Coupon' not in request.POST['apply_remove_coupon']:
                    try:
                        coupon = Coupon.objects.get(
                            code=coupon_code, 
                            active=True, 
                            valid_from__lte=timezone.now(), 
                            valid_to__gte=timezone.now()
                        )
                        discount = coupon.discount / 100 * total
                        total -= discount
                        print(f"Coupon code '{coupon_code}' applied. Discount: {discount}")
                    except Coupon.DoesNotExist:
                        print(f"Coupon code '{coupon_code}' is invalid or expired.")
                        return render(request, 'cart.html', {
                            'cart': order_obj,
                            'coupon_error': "Invalid or expired coupon code.",
                            'addresses': customer.addresses.all()
                        })
                elif 'Remove Coupon' in request.POST['apply_remove_coupon']:
                    total = sum(item.product.discount_price * item.quantity for item in order_obj.added_items.all())
                    print("Coupon removed. Total recalculated.")

                order_obj.total_price = total
                order_obj.save()

                return render(request, 'cart.html', {
                    'cart': order_obj,
                    'total': total,
                    'discount': discount,
                    'addresses': customer.addresses.all()
                })

            order_obj.total_price = total
            order_obj.save()

            context = {
                'order': order_obj,
                'addresses': customer.addresses.all()
            }
            return render(request, 'payment.html', context)

        except Order.DoesNotExist:
            print(f"Order for customer {customer} does not exist.")
            return redirect('cart')

@login_required
def process_payment(request):
    if request.method == "POST":
        user = request.user
        customer = user.customer_profile
        payment_method = request.POST.get('payment_method')
        address_id = request.POST.get('address_id')
        total = request.POST.get('total')

        print(f"POST Data: {request.POST}")
        print(f"Payment method: {payment_method}, Address ID: {address_id}, Total: {total}")

        try:
            address_id = int(address_id)
        except ValueError:
            print(f"Invalid address ID: {address_id}")
            return JsonResponse({'error': 'Invalid address ID'}, status=400)

        try:
            total = float(total)
        except ValueError:
            print(f"Invalid total: {total}")
            return JsonResponse({'error': 'Invalid total'}, status=400)

        try:
            order_obj = Order.objects.get(
                owner=customer,
                order_status=Order.CART_STAGE
            )
            order_obj.payment_method = payment_method
            order_obj.address_id = address_id
            order_obj.total_price = total
            order_obj.save()

            if payment_method == 'cod':
                print(f"Decreasing stock for Order ID: {order_obj.id}")
                order_obj.decrease_stock()
                
                order_obj.order_status = Order.ORDER_CONFIRM
                order_obj.save()
                print(f"Order {order_obj.id} confirmed with total {total}")
                return redirect('payment_success', address_id=address_id, order_id=order_obj.id)
            else:
                host = request.get_host()
                paypal_checkout = {
                    'business': settings.PAYPAL_RECEIVER_EMAIL,
                    'amount': total,
                    'item_name': f'Order {order_obj.id}',
                    'invoice': str(uuid.uuid4()),
                    'currency_code': 'USD',
                    'notify_url': f"http://{host}{reverse('paypal-ipn')}",
                    'return_url': f"http://{host}{reverse('payment_success', kwargs={'address_id': address_id, 'order_id': order_obj.id})}",
                    'cancel_return': f"http://{host}{reverse('payment-failed')}",
                }

                print("PayPal dictionary:", paypal_checkout)
                paypal_payment_button = PayPalPaymentsForm(initial=paypal_checkout)

                context = {
                    'order': order_obj,
                    'paypal': paypal_payment_button,
                }
                return render(request, 'paypal_payment.html', context)

        except Order.DoesNotExist:
            print("Order does not exist for customer")
            return redirect('cart')
    return redirect('cart')



@login_required
def payment_success(request, address_id, order_id):
    user = request.user
    customer = user.customer_profile

    try:
        order = Order.objects.get(id=order_id, owner=customer)
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist for customer {customer.id}")
        return redirect('cart')

    # Get the selected address
    try:
        address = customer.addresses.get(id=address_id)
    except Customer_Address.DoesNotExist:
        print(f"Address with id {address_id} does not exist for customer {customer.id}")
        return redirect('cart')

    address_details = f'{address.name}, {address.street_address}, {address.city}, {address.emirates}, {address.zip_code}, {address.country}, {address.mobile_number}'

    # Update order status if payment method is PayPal
    if order.payment_method == 'paypal':
        order.order_status = Order.ORDER_PROCESSED
        order.save()

    # Prepare email content for customer
    subject_customer = 'Order Confirmation'
    message_customer = f'Thank you for your order!\n\nOrder ID: {order.id}\n\nProducts:\n'
    for item in order.added_items.all():
        message_customer += f'- {item.product.title} ({item.size}): {item.quantity} x AED {item.product.discount_price}\n'
    message_customer += f'\nTotal: AED {order.total_price}\n\nDelivery Address:\n{address_details}'

    # Prepare email content for admin
    subject_admin = 'New Order Received'
    message_admin = f'New order received!\n\nOrder ID: {order.id}\n\nProducts:\n'
    for item in order.added_items.all():
        message_admin += f'- {item.product.title} ({ item.size }): {item.quantity} x AED {item.product.discount_price}\n'
    message_admin += f'\nTotal: AED {order.total_price}\n\nCustomer Details:\n'
    message_admin += f'Email: {customer.user.email}\n'
    message_admin += f'Address: {address_details}\n'
    message_admin += f'Payment Method: {order.payment_method}\n'

    if order.coupons.exists():
        message_admin += 'Coupons Applied:\n'
        for coupon in order.coupons.all():
            message_admin += f'- {coupon.code}: {coupon.discount}% off\n'
    else:
        message_admin += 'No Coupons Applied.\n'

    from_email = 'goldennaina2020ad@gmail.com'
    recipient_list_customer = [user.email]
    recipient_list_admin = ['goldennaina2020.manager@gmail.com']  # Replace with your admin email

    # Send email to customer
    send_mail(subject_customer, message_customer, from_email, recipient_list_customer, fail_silently=False)

    # Send email to admin
    send_mail(subject_admin, message_admin, from_email, recipient_list_admin, fail_silently=False)

    return render(request, 'payment_success.html')








def payment_failed_view(request):
    messages.error(request, 'Payment was cancelled or failed. Please try again.')
    return render(request, 'payment-failed.html')




@login_required
def show_orders(request):
    user = request.user
    customer = user.customer_profile
    all_orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE).order_by('-created_at')
    context = {'orders': all_orders}
    return render(request, 'order.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)
    if request.method == 'POST':
        order.cancel_order()
        return redirect('orders')
    context = {'order': order}
    return render(request, 'cancel_order.html', context)





def Coupons_view(request):
    coupons = Coupon.objects.all()
    context = {'coupons': coupons}
    return render(request, 'coupons.html', context)


@login_required
def request_return(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)

        if order and order.is_within_return_period():
            order.is_returned = True
            order.return_request_date = timezone.now()
            order.save()
            return redirect('request_refund', order_id=order.id)
        else:
            return JsonResponse({'message': 'Order not found or return period has expired.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def request_refund(request, order_id=None):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)

        if order.is_refund_requested:
            return JsonResponse({'message': 'Refund has already been requested for this order.'}, status=400)

        if order:
            order.is_refund_requested = True
            return_reason = request.POST.get('return_reason')
            other_reason = request.POST.get('other_reason')
            if return_reason == 'Other':
                return_reason = other_reason

            order.return_reason = return_reason
            order.bank_name = request.POST.get('bank_name')
            order.account_number = request.POST.get('account_number')
            order.ifsc_code = request.POST.get('ifsc_code')
            order.save()

            # Initiate PayPal refund process here
            return redirect('refund_approved')
        else:
            return JsonResponse({'message': 'Order not found or not eligible for refund.'}, status=404)
    elif request.method == 'GET' and order_id:
        order = get_object_or_404(Order, id=order_id, owner=request.user.customer_profile)
        if order.is_refund_requested:
            return render(request, 'refund_already_requested.html', {'order': order})
        return render(request, 'refund.html', {'order': order})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)
    

@login_required
def refund_approved(request):
    user = request.user
    customer = user.customer_profile

    # Retrieve the most recent refund request
    order = Order.objects.filter(owner=customer).order_by('-return_request_date').first()
    
    if not order:
        return redirect('some_error_page')  # Handle error appropriately

    # Prepare email content for customer
    subject_customer = 'Refund Request Approved'
    message_customer = f'Your refund request has been approved!\n\nOrder ID: {order.id}\n\nDetails of your refund will be processed shortly.\n'
    
    if order.is_returned:
        message_customer += 'Reason for Return: {}\n'.format(order.return_reason or 'N/A')
        message_customer += 'Bank Name: {}\n'.format(order.bank_name or 'N/A')
        message_customer += 'Account Number: {}\n'.format(order.account_number or 'N/A')
        message_customer += 'IFSC Code: {}\n'.format(order.ifsc_code or 'N/A')

    # Prepare email content for admin
    subject_admin = 'Refund Request Approved'
    message_admin = f'Refund request has been approved!\n\nOrder ID: {order.id}\n\nDetails of the refund:\n'
    
    if order.is_returned:
        message_admin += 'Reason for Return: {}\n'.format(order.return_reason or 'N/A')
        message_admin += 'Bank Name: {}\n'.format(order.bank_name or 'N/A')
        message_admin += 'Account Number: {}\n'.format(order.account_number or 'N/A')
        message_admin += 'IFSC Code: {}\n'.format(order.ifsc_code or 'N/A')
        message_admin += f'Customer Email: {customer.user.email}\n'

    from_email = 'goldennaina2020ad@gmail.com'
    recipient_list_customer = [user.email]
    recipient_list_admin = ['goldennaina2020.manager@gmail.com']  # Replace with your admin email

    # Send email to customer
    send_mail(subject_customer, message_customer, from_email, recipient_list_customer, fail_silently=False)

    # Send email to admin
    send_mail(subject_admin, message_admin, from_email, recipient_list_admin, fail_silently=False)

    return render(request, 'refund_approved.html')

    