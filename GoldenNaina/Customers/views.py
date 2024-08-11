from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Customer, Customer_Address, ContactUs, Profile
from django.contrib import messages
from orders.models import Order
from products.models import Product
from orders.models import Order, OrderedItem
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ProfileForm, AddressForm, ContactUsForm
from django.conf import settings


# account views

def sign_out(request):
    logout(request)
    return redirect('/')

def Account(request):
    context = {}

    if request.method == 'POST':
        if 'register' in request.POST:
            context['register'] = True
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                
                # Check if the email is already in use
                if User.objects.filter(email=email).exists():
                    raise ValueError("Email already in use")
                
                # Create user
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()

                # Create customer account
                customer = Customer.objects.create(name=username, user=user)
                customer.save()

                messages.success(request, 'Account created successfully. You can now log in.')
                return redirect('Account')
            except ValueError as e:
                context['error'] = str(e)
                messages.error(request, context['error'])
            except Exception as e:
                context['error'] = "Well, Login"
                messages.error(request, context['error'])
                return redirect('Account')

        elif 'login' in request.POST:
            context['register'] = False
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                context['error'] = 'Invalid username or password.'
                messages.error(request, context['error'])

    return render(request, 'account.html', context)

# customer dashboard

@login_required
def customer_dashboard(request):
    user = request.user
    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=user, defaults={
        'full_name': user.get_full_name(),  # Use a suitable default if available
        'bio': '',
        'phone': '',
        
    })
    
    # Ensure customer_profile exists
    try:
        customer = user.customer_profile
    except Profile.DoesNotExist:
        customer = Profile.objects.create(user=user, full_name=user.get_full_name())

    addresses = customer.addresses.all() 
    orders = Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    
    context = {
        'orders': orders,
        'addresses': addresses,
        'profile': profile,
    }
    return render(request, 'customer_dashboard.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_update.html', {'form': form, 'profile': profile})

# order section

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    ordered_items = order.added_items.all()  # Fetch related ordered items
    context = {
        'order': order,
        'ordered_items': ordered_items,
    }
    return render(request, 'order_detail.html', context)

# address section

@login_required
def address_list(request):
    addresses = request.user.customer_profile.addresses.all()
    return render(request, 'address_list.html', {'addresses': addresses})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user.customer_profile
            address.save()
            return redirect('process_payment')
    else:
        form = AddressForm()

    return render(request, 'add_address.html', {'form': form})



@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Customer_Address, id=address_id, customer=request.user.customer_profile)
    
    # Check if the current user has permission to edit the address
    if address.customer != request.user.customer_profile:
        return HttpResponseForbidden("You don't have permission to edit this address.")
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('process_payment')
    else:
        form = AddressForm(instance=address)
    
    context = {'form': form}
    return render(request, 'edit_address.html', context)


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Customer_Address, id=address_id)
    
    # Debug information
    print(f"Address owner: {address.customer}")
    print(f"Current user: {request.user.customer_profile}")

    if address.customer != request.user.customer_profile:
        # Address does not belong to the current user
        return HttpResponseForbidden("You are not allowed to delete this address.")
    
    if request.method == 'POST':
        address.delete()
        return redirect('dashboard')
    
    context = {'address': address}
    return render(request, 'delete_address.html', context)


def contact_us_view(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save()
            # Send email to admin
            send_mail(
                subject=f"New Contact Us Message from {contact.full_name}",
                message=f"Subject: {contact.subject}\n\nMessage:\n{contact.message}\n\nContact Information:\nName: {contact.full_name}\nEmail: {contact.email}\nPhone: {contact.phone}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            return redirect('contact_success')
    else:
        form = ContactUsForm()
    
    return render(request, 'contact_us.html', {'form': form})