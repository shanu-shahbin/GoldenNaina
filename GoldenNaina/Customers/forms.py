from django import forms
from .models import Customer_Address, ContactUs, Profile

class PasswordResetForm(forms.Form):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data


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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'image', 'phone']

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone', 'subject', 'message']