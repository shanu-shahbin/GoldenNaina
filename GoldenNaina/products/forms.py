from django import forms
from django.forms import ModelForm
from.models import ProductReview


class ProductReviewForm(ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Write your review here...'}))

    class Meta:
        model = ProductReview
        fields = ['rating','review']            