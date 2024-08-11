from django.db import models

# Create your models here.

# class About_company(models.Model):
#     name = models.CharField(max_length=200)
#     title = models.CharField(max_length=200)
#     about = models.TextField()
#     image = models.ImageField(upload_to='about_company/')
#     year = models.IntegerField()
#     history = models.TextField()

#     def __str__(self):
#         return self.name
    
# class Terms_of_use(models.Model):
#     name = models.CharField(max_length=200)
#     title = models.CharField(max_length=200)
#     about = models.TextField()
#     term_1 = models.CharField(max_length=200)
#     term_2 = models.CharField(max_length=200)
#     term_3 = models.CharField(max_length=200)
#     term_4 = models.CharField(max_length=200)
#     term_5 = models.CharField(max_length=200)
#     term_6 = models.CharField(max_length=200)
#     term_1_description = models.TextField()
#     term_2_description = models.TextField()
#     term_3_description = models.TextField()
#     term_4_description = models.TextField()
#     term_5_description = models.TextField()
#     term_6_description = models.TextField()

#     def __str__(self):
#         return self.name
# class Privacy_policy(models.Model):
#     name = models.CharField(max_length=200)
#     title = models.CharField(max_length=200)
#     about = models.TextField()
#     privacy_1 = models.CharField(max_length=200)
#     privacy_2 = models.CharField(max_length=200)
#     privacy_3 = models.CharField(max_length=200)
#     privacy_4 = models.CharField(max_length=200)
#     privacy_5 = models.CharField(max_length=200)
#     privacy_1_description = models.TextField()
#     privacy_2_description = models.TextField()
#     privacy_3_description = models.TextField()
#     privacy_4_description = models.TextField()
#     privacy_5_description = models.TextField()
#     def __str__(self):
#         return self.name
    


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
