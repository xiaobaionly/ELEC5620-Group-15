from pathlib import Path
import environ, os

# ----------------------------------------------------------------------
# Base directory of the project
# ----------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# Load environment variables from .env file
# ----------------------------------------------------------------------
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# ----------------------------------------------------------------------
# Security & Debug settings
# ----------------------------------------------------------------------
# Read from .env; fallback to default for local/dev
SECRET_KEY = env("SECRET_KEY", default="dev-key-change-me")
DEBUG = env.bool("DEBUG", default=True)

# Allow multiple hosts, split by comma
# e.g. 127.0.0.1,localhost,0.0.0.0
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="127.0.0.1,localhost").split(",")]

# ----------------------------------------------------------------------
# Installed applications
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Middleware configuration
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Root URL configuration
# ----------------------------------------------------------------------
ROOT_URLCONF = 'core.urls'

# ----------------------------------------------------------------------
# Template engine configuration
# ----------------------------------------------------------------------
TEMPLATES = [
    {
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
    },
]

# ----------------------------------------------------------------------
# WSGI application
# ----------------------------------------------------------------------
WSGI_APPLICATION = 'core.wsgi.application'

# ----------------------------------------------------------------------
# Database configuration
# ----------------------------------------------------------------------
# Prefer DATABASE_URL from .env (e.g. sqlite:///db.sqlite3 or postgres://user:pass@host/db)
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# ----------------------------------------------------------------------
# Static & Media files
# ----------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------------------------------------------------
# Custom user model
# ----------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.User'

# ----------------------------------------------------------------------
# Authentication URLs
# ----------------------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/route/'
LOGOUT_REDIRECT_URL = '/'

# ----------------------------------------------------------------------
# Admin Customization
# ----------------------------------------------------------------------
# Change Django admin site titles safely after the app registry is ready
from django.apps import apps
from django.contrib import admin

def customize_admin_titles():
    """Customize Django admin site titles safely after app registry is ready."""
    admin.site.site_header = "AgriMate Administration"
    admin.site.site_title = "AgriMate Admin Portal"
    admin.site.index_title = "Welcome to AgriMate Control Panel"

# Apply customization immediately if apps are loaded
try:
    if apps.ready:
        customize_admin_titles()
except Exception:
    # Avoid interfering with initial app loading
    pass

# ----------------------------------------------------------------------
# Optional: LLM API configuration
# ----------------------------------------------------------------------
# These variables can be accessed anywhere in your code
LLM_PROVIDER = env('LLM_PROVIDER', default='openai')
LLM_MODEL = env('LLM_MODEL', default='gpt-4.1-mini')
LLM_API_KEY = env('LLM_API_KEY', default='')
