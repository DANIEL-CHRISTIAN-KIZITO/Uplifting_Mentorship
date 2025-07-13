import os
from pathlib import Path
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-secret-key-here' # **CHANGE THIS IN PRODUCTION**

DEBUG = True # Set to False in production

ALLOWED_HOSTS = ['*'] # **CHANGE THIS IN PRODUCTION to your domain(s)**

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts', # Your custom user app
    'mentorship',
    'scheduling_sessions',
    'chat',
    'progress',
    'feedback',
    'dashboard', # Your dashboard app
    'api',
    #'corsheaders', # For CORS if you have a separate frontend
    'rest_framework', # For API development
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'corsheaders.middleware.CorsMiddleware', # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uplifting_mentorship.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Project-wide templates directory
        'APP_DIRS': True, # Allows Django to find templates in app-specific 'templates' folders
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'uplifting_mentorship.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'uplifting_db',
        'USER': 'uplifting_user',
        'PASSWORD': 'Danjr77#',
        'HOST': 'localhost',
        'PORT': '5432',  # Or your custom port if you changed it
    }
}


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
TIME_ZONE = 'Africa/Kampala' # Set your local timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # Collect static files here in production
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Project-level static files
]

# Media files (user-uploaded content)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Authentication URLs
LOGIN_URL = 'accounts:login' # URL name for the login page
LOGIN_REDIRECT_URL = 'accounts:dashboard_home' # URL name to redirect after successful login
LOGOUT_REDIRECT_URL = 'accounts:login' # URL name to redirect after logout

# Messages Framework Tags (for styling messages in templates)
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Email Backend for Password Reset (for development, prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# For production, you'd use a real SMTP backend:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.yourprovider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your_email@example.com'
# EMAIL_HOST_PASSWORD = 'your_email_password'
# DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
