"""
Django settings for snappy_backend project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY & DEBUG
# ==============================================================================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-3o5$w&e2b&-9ob66%vb^7$38d0qu!nv#&8)efonx9sgc)la0d!')

# Set to False in your ECS Environment Variables
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*'] # Update with your ELB DNS or domain in production


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

DJANGO_APPS = [
    'daphne', # Daphne must be at the top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
    'drf_yasg',
    'corsheaders',
    'channels',
]

LOCAL_APPS = [
    "apps.testapp",
    "apps.user",
    "apps.portal",
    "apps.news", # Added based on your NewsConsumer/routing
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'snappy_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'snappy_backend.wsgi.application'
ASGI_APPLICATION = 'snappy_backend.asgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

# Switching to Environment variables for DB if available, else SQLite
DB_NAME = os.getenv('DB_NAME')
if DB_NAME:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==============================================================================
# REDIS / CELERY / CHANNELS (Dynamic Local vs Cloud)
# ==============================================================================

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')

# This is the master switch: False for Local Docker, True for AWS ECS
REDIS_USE_SSL = os.environ.get('REDIS_USE_SSL', 'False').lower() == 'true'

if REDIS_USE_SSL:
    # AWS ElastiCache Path
    REDIS_PROTOCOL = 'rediss'
    SSL_CERT_SETTING = '?ssl_cert_reqs=CERT_NONE'
    CELERY_USE_SSL_DICT = {'ssl_cert_reqs': None}
else:
    # Local Docker Path
    REDIS_PROTOCOL = 'redis'
    SSL_CERT_SETTING = ''
    CELERY_USE_SSL_DICT = None

# Single URL used by both Celery and Channels
REDIS_URL = f"{REDIS_PROTOCOL}://{REDIS_HOST}:{REDIS_PORT}/0{SSL_CERT_SETTING}"

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_USE_SSL = CELERY_USE_SSL_DICT
CELERY_REDIS_BACKEND_USE_SSL = CELERY_USE_SSL_DICT
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_WORKER_ENABLE_REMOTE_CONTROL = False
CELERY_BROKER_TRANSPORT_OPTIONS = {'global_keyprefix': '{celery}'}

# Channel Layers (WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL],
        },
    },
}


# ==============================================================================
# EMAIL
# ==============================================================================

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'sandbox.smtp.mailtrap.io')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 2525))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')


# ==============================================================================
# CORS & STATIC
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# AUTH & I18N
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
