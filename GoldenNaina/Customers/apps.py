from django.apps import AppConfig

class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Customers'

    def ready(self):
        import Customers.signals
