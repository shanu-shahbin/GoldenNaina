from datetime import timedelta
from pathlib import Path
import os
import smtplib


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-zb(tk4yuenb+2x!-5^^s_plirr#mi^saiurs4vm2(^-mn%=*_-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'HomeApp',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Customers',
    'products',
    'orders',
    'taggit',
    'ckeditor',
    'paypal.standard.ipn',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',

]

ROOT_URLCONF = 'GoldenNaina.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'products.context_processors.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
                'orders.context_processors.cart_item_count',
                'Customers.context_processors.customer_addresses',
                'HomeApp.context_processors.social_links',            
            ],
        },
    },
]

WSGI_APPLICATION = 'GoldenNaina.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'goldennaina',
        'USER': 'goldennaina',
        'PASSWORD': 'goldennaina',
        'HOST': 'goldennaina.cd6yi4yci4yn.us-west-2.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR,  'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_header': 'GoldenNaina Admin',
    'site_brand': 'Golden Naina',
    'site_logo': 'images/Jazmin_profile.jpeg',
    
    }

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': 800,
        'skin': 'moono',
        'codeSnippet_theme': 'monokai',
        'extraPlugins': ','.join([
            'codesnippet', 'widget', 'lineutils', 'clipboard', 
            'dialog', 'dialogui', 'contextmenu', 'autogrow', 
            'exportfile', 'filebrowser', 'html5filebrowser', 
            'image', 'image2', 'imagebrowser', 'imageupload', 
            'smiley', 'template', 'templatestyles', 'toolbar'
        ]),
    }
}


LOGIN_URL = 'Account'


AUTO_LOGOUT = {
    'IDLE_TIME': 15 * 60,  
    'MESSAGE': 'The session has expired. Please login again to continue.',
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'goldennaina2020ad@gmail.com'
EMAIL_HOST_PASSWORD = 'vyah gyjc flks oeyj'
DEFAULT_FROM_EMAIL = 'goldennaina2020ad@gmail.com'
ADMIN_EMAIL = 'goldennaina2020.manager@gmail.com'  

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("SMTP connection successful")
    server.quit()
except Exception as e:
    print(f"SMTP connection failed: {e}")



PAYPAL_RECEIVER_EMAIL = 'sb-jchvu14723533@business.example.com' 
PAYPAL_TEST = True