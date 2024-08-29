from .models import Footer, Company_address, Footer_Popular_Search

def social_links(request):
    return {
        'social_links': Footer.objects.all(),
        'company_address': Company_address.objects.all(),
        'footer_popular_searches': Footer_Popular_Search.objects.all()
    }    