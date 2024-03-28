
from datetime import timedelta
import os
from pathlib import Path
import environ
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


env = environ.Env()
# Read .env file
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DJANGO_DEBUG', default=False)
SECURE_SSL_REDIRECT=env.bool('SECURE_SSL_REDIRECT', default=False)
SECURE_BROWSER_XSS_FILTER=env.bool('SECURE_BROWSER_XSS_FILTER', default=False)
CORS_ALLOWED_ORIGINS = env.str('CORS_ALLOWED_ORIGINS', default='https://localhost:8080').split(',')
CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS', default=True)

DEFAULT_AUTHENTICATION_CLASSES =  ['rest_framework.authentication.TokenAuthentication', 'rest_framework.authentication.SessionAuthentication']
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', 
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'app',  
]

MIDDLEWARE = [
  
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mrjohnnyrocha.urls'

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

WSGI_APPLICATION = 'mrjohnnyrocha.wsgi.application'

DATABASES = {
    'default': env.db(),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # Add any other authentication classes here
    ),
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
AUTH_USER_MODEL = 'app.CustomUser'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ORIGIN_WHITELIST=['https://localhost:8080','https://mrjohnnyrocha.com','https://localhost:8081']

SIMPLE_JWT = {
    'AUTH_HEADER_PREFIX': 'Bearer',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Adjust token expiration time
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Adjust refresh token expiration

}

import boto3

AWS_ACCESS_KEY_ID = 'AKIA2UC3EKPAN2OWSGSI'  # Replace with your AWS credentials
AWS_SECRET_ACCESS_KEY = 'yiHhjIkONaJ1PsIvB6AE4uBtxUbzDgwgkoUeL0w3'  # Replace with your AWS credentials
AWS_STORAGE_BUCKET_NAME = 'mrjohnnyrocha-backend'  # Replace with your S3 bucket name
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}  # Optional: Set cache headers

STATIC_ROOT = 's3://%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN  # Use HTTPS for secure delivery
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'