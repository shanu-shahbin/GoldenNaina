from .models import Footer, Company_address

def social_links(request):
    return {
        'social_links': Footer.objects.all(),
        'company_address':Company_address.objects.all()
    }