from pathlib import Path
import environ, os

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Security key (Change this in production)
SECRET_KEY = 'dev-key-change-me'

# Debug mode (set to False in production)
DEBUG = True

# Allowed hosts for this application
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Installed applications
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'django_htmx',

    # Custom apps
    'accounts',
    'products',
    'qa',
    'pricing',
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration
ROOT_URLCONF = 'core.urls'

# Template engine configuration
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# WSGI application entry point
WSGI_APPLICATION = 'core.wsgi.application'

# Database configuration — using SQLite (zero setup for local development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/route/'
LOGOUT_REDIRECT_URL = '/'


# Admin Customization (Safe Way)
# These lines must run after Django apps are ready.
# Therefore, we wrap them inside a function connected to AppConfig.ready()

from django.apps import apps
from django.contrib import admin

def customize_admin_titles():
    """Customize Django admin site titles safely after app registry is ready."""
    admin.site.site_header = "AgriMate Administration"
    admin.site.site_title = "AgriMate Admin Portal"
    admin.site.index_title = "Welcome to AgriMate Control Panel"

# If apps are already loaded (e.g. during manage.py runserver), apply immediately
try:
    if apps.ready:
        customize_admin_titles()
except Exception:
    # Avoid interfering with initial app loading
    pass