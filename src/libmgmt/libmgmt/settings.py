import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

import socket
import psycopg2
import psycopg2.extensions
import psycopg2.extras

# Load environment variables
load_dotenv()

# === BASE SETTINGS ===
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-n+q2eeten^k$75pyf^4i9%@^j)7)_l8g#kml@g-7uhx0ji2(fx")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = [
    "lybrarymanagementsystem.onrender.com",
    "localhost",
    "127.0.0.1",
]

def force_ipv4():
    original_getaddrinfo = socket.getaddrinfo
    def getaddrinfo_ipv4(*args, **kwargs):
        return original_getaddrinfo(*args, family=socket.AF_INET, **kwargs)
    socket.getaddrinfo = getaddrinfo_ipv4

force_ipv4()

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'libapp',
    'bookapp',
    'borrow',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'libmgmt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CORS_ALLOW_ALL_ORIGINS = True
ROOT_URLCONF = 'libmgmt.urls'
WSGI_APPLICATION = 'libmgmt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if os.getenv("DATABASE_URL"):
    # Supabase / Render (Production)
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True  # Supabase needs SSL
        )
    }
else:
    # Local PostgreSQL (Development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'newlibdb'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
CSRF_TRUSTED_ORIGINS = ["https://lybrarymanagementsystem.onrender.com"]
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# === LANGUAGE / TIMEZONE ===
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# === STATIC / MEDIA FILES ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Whitenoise optimized static storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'libapp.User'


LOGOUT_REDIRECT_URL = "login"
LOGIN_URL = 'login'  # matches your urls.py name
LOGIN_REDIRECT_URL = 'dashboard'  # optional

