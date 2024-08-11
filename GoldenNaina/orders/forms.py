from django import forms
from Customers.models import Customer_Address



class AddressForm(forms.ModelForm):
    class Meta:
        model = Customer_Address
        fields = ['street_address', 'city', 'state', 'postal_code', 'country', 'address_type']