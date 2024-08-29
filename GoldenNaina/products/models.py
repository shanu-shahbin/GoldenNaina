from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Avg
from django.core.exceptions import ValidationError
from django.urls import reverse




RATING = (
    (1, '🌟'),
    (2, '🌟🌟'),
    (3, '🌟🌟🌟'),
    (4, '🌟🌟🌟🌟'),
    (5, '🌟🌟🌟🌟🌟')
)



class Size(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories', null=True)
    percentage = models.IntegerField(default=0, null=True) # remove null later


    def __str__(self):
        return self.name

class Product(models.Model):
    LIVE = 1
    DELETE = 0
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Delete'))

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(upload_to='media/')
    priority = models.IntegerField(default=0)
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(default=5)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    return_policy = models.TextField(blank=True, null=True, help_text='Return policy in days', default='7')

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.discount_price and self.discount_price > self.price:
            raise ValidationError("Discount price should not be greater than the price")

    def get_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def get_rating_stars(self):
        return '⭐' * self.rating

    def get_average_rating(self):
        avg_rating = self.reviews.aggregate(average=Avg('rating'))['average']
        return avg_rating if avg_rating else 5

    def get_average_rating_stars(self):
        return '⭐' * round(self.get_average_rating())

    def get_stock_for_size(self, size):
        try:
            stock = self.stocks.get(size=size)
            return stock.quantity
        except Stock.DoesNotExist:
            return 0


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.size.name}: {self.quantity}"


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_images', null=True)
    images = models.ImageField(upload_to='product_images', null=True)

    class Meta:
        ordering = ['-id']

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING, default=None)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Product Reviews'
  
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='wishlist_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        return self.product.title if self.product else 'No Product'

class Theme_model(models.Model):
    image = models.ImageField(upload_to='theme_models')
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


class PopularSearch(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, help_text="Enter the URL or name of the view to link to")

    def __str__(self):
        return self.name

    def get_url(self):
        try:
            return reverse(self.url)
        except:
            return self.url  # Return the URL as is if it's not a view name