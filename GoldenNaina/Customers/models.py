from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Customer_Address(models.Model):
    name = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    street_address = models.CharField(max_length=255)  # P.O Box
    city = models.CharField(max_length=100, default='AbuDubai')  # Default to Dubai
    emirates = models.CharField(max_length=100, default='AbuDubai')  # Default to Dubai
    zip_code = models.CharField(max_length=20)  # Zip code
    country = models.CharField(max_length=100, default='United Arab Emirates')  
    mobile_number = models.CharField(max_length=20)  # 971-(1)968565699
    address_type = models.CharField(max_length=10, choices=(('Home', 'Home'), ('Work', 'Work')), default='Home')

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.emirates}, {self.zip_code}, {self.country}, {self.address_type}, {self.mobile_number}, {self.name}"

    

class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
    
    def __str__(self) -> str:
        return self.full_name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name


