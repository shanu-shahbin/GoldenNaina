from .models import *
from django.shortcuts import render



def faq(request):
    return render(request, 'faq.html')

def terms_and_conditions(request):
    terms = TermsAndConditions.objects.all()
    return render(request, 'tc.html', {'terms': terms})


def Social_links(request):
    social_links = Footer.objects.all()
    company_address = Company_address.objects.all()

    context = {
        'social_links': social_links,
        'company_address': company_address,
    }
    
    return render(request, 'footer.html', context)
