from django import forms
from Customers.models import Customer_Address



class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer_Address
        fields = [
            'name', 
            'street_address', 
            'city', 
            'emirates', 
            'zip_code', 
            'country', 
            'address_type', 
            'mobile_number'
        ]
