from django.db import models
from django.urls import reverse

class TermsAndConditions(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    period = models.CharField(max_length=255)
    offer_details = models.TextField()
    conditions = models.TextField()

    def conditions_list(self):
        return self.conditions.split(';')

    def __str__(self):
        return self.title
    
class Footer(models.Model):
    facebook_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    instagram_link = models.URLField(max_length=200, blank=True)
    whatsapp_link = models.URLField(max_length=200, blank=True)

    
class Company_address(models.Model):
    location = models.CharField(max_length=355)
    email = models.EmailField(max_length=54)
    phone_number = models.CharField(max_length=20)

class Career(models.Model):
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField()
    date_posted = models.DateField(auto_now_add=True)
    last_date_to_apply = models.DateField()

    def __str__(self):
        return self.job_title

class Footer_Popular_Search(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, help_text="Enter the URL for footer popular search")

    def __str__(self):
        return self.name

    def get_url(self):
        try:
            return reverse(self.url)
        except:
            return self.url