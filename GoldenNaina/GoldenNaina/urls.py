from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('', include('Customers.urls')),
    path('', include('orders.urls')),
    path('', include('HomeApp.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('paypal.standard.ipn.urls')),
]



if settings.DEBUG:
    urlpatterns +=static(settings.STATIC_URL,
                         document_root=settings.STATIC_ROOT)
    urlpatterns +=static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)