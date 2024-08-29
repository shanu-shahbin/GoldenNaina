from .models import *
from django.shortcuts import render
from .models import Footer_Popular_Search, Career


def faq(request):
    return render(request, 'faq.html')

def terms_and_conditions(request):
    terms = TermsAndConditions.objects.all()
    return render(request, 'tc.html', {'terms': terms})


def Social_links(request):
    footer_popular_searches = Footer_Popular_Search.objects.all()
    social_links = Footer.objects.all()
    company_address = Company_address.objects.all()

    context = {
        'social_links': social_links,
        'company_address': company_address,
        'footer_popular_searches': footer_popular_searches,

    }
    
    return render(request, 'footer.html', context)

def terms_and_use(request):
    return render(request, 'terms_of_use.html')

def Privacy_policy(request):
    return render(request, 'privacy_policy.html')

def WhiteHat(request):
    return render(request, 'whitehat.html')

def careers(request):
    careers = Career.objects.all()
    recent_email = careers.last().email if careers.exists() else None 
    return render(request, 'careers.html', {'careers': careers, 'recent_email': recent_email})

def about_us(request):
    return render(request, 'about.html')


