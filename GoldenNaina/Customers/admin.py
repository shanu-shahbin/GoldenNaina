from django.contrib import admin
from .models import Customer, Customer_Address, ContactUs, Profile


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name', 'phone')


class Customer_AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'name', 'street_address', 'city', 'emirates', 'zip_code', 'country', 'address_type', 'mobile_number')
    search_fields = ('customer__name', 'street_address', 'city', 'emirates', 'zip_code', 'country')


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone')
    search_fields = ('full_name', 'email', 'phone', 'subject')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'bio', 'image', 'created_at', 'updated_at')  
    search_fields = ('full_name', 'bio')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Customer_Address, Customer_AddressAdmin)
