from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    # Credentials paths
    
    path('account/', views.Account, name='Account'),
    path('logout/', views.sign_out, name='Logout'),


    # password reset paths

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Customer paths

    path('customer_dashboard/', views.customer_dashboard, name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    
    path('order/<int:pk>/', views.order_detail, name='order_detail'),

    # Address paths
    path('addresses/', views.address_list, name='address_list'),
    path('add_address/', views.add_address, name='add_address'), 
    path('edit_address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    

    # Contact paths
    path('contact-us/', views.contact_us_view, name='contact_us'),
    path('contact-success/', TemplateView.as_view(template_name='contact_success.html'), name='contact_success'),
    
]
