
from django.contrib import admin
from .models import TermsAndConditions, Footer, Company_address, Career

class CareerAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'location', 'date_posted', 'last_date_to_apply')
    search_fields = ('job_title', 'location')
    list_filter = ('location', 'date_posted')
    ordering = ('-date_posted',)

admin.site.register(TermsAndConditions)
admin.site.register(Footer)
admin.site.register(Company_address)
admin.site.register(Career, CareerAdmin)
