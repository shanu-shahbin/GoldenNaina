
from django.urls import path, include
from . import views

urlpatterns = [
    
   path('faq/', views.faq, name='faq'),
   path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
   path('socials/',views.Social_links,name='footer'),
   
]

