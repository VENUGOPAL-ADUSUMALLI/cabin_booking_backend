"""
Django settings for cabin_booking_backend project.
"""
import os
from pathlib import Path
import pymysql
from django.conf.urls.static import static
from sentry_sdk import init as sentry_sdk_init

# Initialize MySQL connector
pymysql.install_as_MySQLdb()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
SECRET_KEY = 'django-insecure-df)(vrdzh)z!8n)d*lyjy37ywq5_3oh^^&7)l)l-b0@qm_09fv'
DEBUG = False
ALLOWED_HOSTS = ['*']
# 'onbwa7m4cf.execute-api.ap-south-1.amazonaws.com', '127.0.0.1'
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cabin_booking',
    'oauth2_provider',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    "storages",
]

# REST Framework & OAuth Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'superuser': 'SuperUser scope'}
}
SIMPLE_JWT = {
    'USER_ID_FIELD': 'user_id',
}

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# URL Configuration
ROOT_URLCONF = 'cabin_booking_backend.urls'

# Templates
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

# WSGI Application
WSGI_APPLICATION = 'cabin_booking_backend.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '3306',
    }
}

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Authentication Model
AUTH_USER_MODEL = 'cabin_booking.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = False

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True

# Static and Media Files on S3

# Media files

# Application and Client Config
APPLICATION_NAME = 'cabin_booking'
CLIENT_ID = "s8o4OHGhpZDdHnSwirlyCIhr1HYafB4UsOTtnAVnj"
CLIENT_SECRET = "ZjL7Mo8pL3XZUi2V1u26lL8Wh1Z6ZX7JoVV3O8MPsxwmwQXW4lR9CEom3j3d9onyxbiffEleTwig9areLEDy9PqsC9OjJNDI7HTL6IEtiALAWleGxTumBdQuipXo"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
REFRESH_TOKEN_EXPIRE_SECONDS = 86400

# Sentry SDK
sentry_sdk_init(
    dsn="https://50cb9481338759ed65ec5b6572452fe5@o4508176376856576.ingest.us.sentry.io/4508176382951425",
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)
STATIC_URL = '/static/'

USE_S3 = bool(os.environ.get("USE_S3_STATIC", "False"))

if USE_S3 is True:
    AWS_ACCESS_KEY_ID = os.environ.get("CUSTOM_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("CUSTOM_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')