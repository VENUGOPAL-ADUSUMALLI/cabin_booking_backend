"""
Django settings for cabin_booking_backend project.

Generated by 'django-admin startproject' using Django 4.2.14.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-df)(vrdzh)z!8n)d*lyjy37ywq5_3oh^^&7)l)l-b0@qm_09fv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

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
    'django_s3_storage'
]
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
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'superuser': 'SuperUser scope'}
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'cabin_booking_backend.urls'

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

WSGI_APPLICATION = 'cabin_booking_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cabin_booking_backend',
        'USER': 'venugopal',
        'PASSWORD': 'venu@12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
SIMPLE_JWT = {
    'USER_ID_FIELD': 'user_id',
    # other settings...
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'cabin_booking.User'
APPLICATION_NAME = 'cabin_booking'
CLIENT_ID = "s8o4OHGhpZDdHnSwirlyCIhr1HYafB4UsOTtnAVnj"
CLIENT_SECRET = "ZjL7Mo8pL3XZUi2V1u26lL8Wh1Z6ZX7JoVV3O8MPsxwmwQXW4lR9CEom3j3d9onyxbiffEleTwig9areLEDy9PqsC9OjJNDI7HTL6IEtiALAWleGxTumBdQuipXo"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
REFRESH_TOKEN_EXPIRE_SECONDS = 86400
CORS_ALLOW_ALL_ORIGINS = True
# curl -X POST -d "grant_type=password&username=<your-username>&password=<your-password>&client_id=s8o4OHGhpZDdHnSwirlyCIhr1HYafB4UsOTtnAVnj&client_secret=ZjL7Mo8pL3XZUi2V1u26lL8Wh1Z6ZX7JoVV3O8MPsxwmwQXW4lR9CEom3j3d9onyxbiffEleTwig9areLEDy9PqsC9OjJNDI7HTL6IEtiALAWleGxTumBdQuipXo" http://<your-domain>/o/token/

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')  # Use the name of your staging environment (e.g. production)
WHITENOISE_STATIC_PREFIX = '/static/'
YOUR_S3_BUCKET = "zappa-static"

STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET

# These next two lines will serve the static files directly
# from the s3 bucket
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# OR...if you create a fancy custom domain for your static files use:
# AWS_S3_PUBLIC_URL_STATIC = "https://static.zappaguide.com/"
import sentry_sdk

sentry_sdk.init(
    dsn="https://50cb9481338759ed65ec5b6572452fe5@o4508176376856576.ingest.us.sentry.io/4508176382951425",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)
