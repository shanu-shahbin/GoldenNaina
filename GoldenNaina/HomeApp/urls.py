from django.urls import path
from . import views
from django.shortcuts import render
from django.conf.urls import handler404


urlpatterns = [
    path('faq/', views.faq, name='faq'),
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('socials/', views.Social_links, name='footer'),
    path('termsUse/', views.terms_and_use, name='terms_use'),
    path('privacy/', views.Privacy_policy, name='privacy'),
    path('whitehat/', views.WhiteHat, name='whitehat'),
    path('careers/', views.careers, name='careers'),
    path('about/', views.about_us, name='about_us'),
]



handler404 = views.custom_404_view
handler500 = views.custom_500_view
