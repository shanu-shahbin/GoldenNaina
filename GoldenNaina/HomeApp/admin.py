
from django.contrib import admin
from .models import TermsAndConditions, Footer, Company_address, Career, Footer_Popular_Search

class CareerAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'location', 'date_posted', 'last_date_to_apply')
    search_fields = ('job_title', 'location')
    list_filter = ('location', 'date_posted')
    ordering = ('-date_posted',)

class Footer_Popular_SearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

admin.site.register(TermsAndConditions)
admin.site.register(Footer)
admin.site.register(Company_address)
admin.site.register(Career, CareerAdmin)
admin.site.register(Footer_Popular_Search, Footer_Popular_SearchAdmin)
