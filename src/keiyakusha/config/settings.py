"""
For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
import os

from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'kick me')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = json.loads(os.environ.get('DJANGO_DEBUG', 'false'))

ALLOWED_HOSTS = json.loads(os.environ.get('DJANGO_ALLOWED_HOSTS', '["*"]'))

if not DEBUG:
    if SECRET_KEY == 'kick me':
        raise ImproperlyConfigured(
            'You must set `DJANGO_SECRET_KEY` outside of debug'
            ' environments.'
        )

    if '*' in ALLOWED_HOSTS:
        raise ImproperlyConfigured(
            'You must set `DJANGO_ALLOWED_HOSTS` to some json-encoded'
            ' array not containing `"*"` outside of debug'
            ' environments.'
        )

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'annoying',
    'django_tables2',
    'widget_tweaks',

    'bank_accounts',
    'clients',
    'engagements',
    'invoices',
    'timing',
    'timing_website',
    'users',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'website.middleware.user_timezone_middleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'keiyakusha_db'),
        'USER': os.environ.get('DJANGO_DB_USER', 'keiyakusha'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASS', 'keiyakusha_password'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'db'),
        'PORT': os.environ.get('DJANGO_DB_PORT', ''),
        'TEST': {
            'NAME': os.environ.get('DJANGO_DB_NAME', 'keiyakusha') + '_test',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators


_namespaced_password_validators = {
    'django.contrib.auth.password_validation': [
        {
            'NAME': 'UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'MinimumLengthValidator',
        },
        {
            'NAME': 'CommonPasswordValidator',
        },
        {
            'NAME': 'NumericPasswordValidator',
        },
    ],
}

AUTH_PASSWORD_VALIDATORS = []

for namespace, members in _namespaced_password_validators.items():
    for member in members:
        member['NAME'] = f'{namespace}.{member["NAME"]}'

        AUTH_PASSWORD_VALIDATORS.append(member)


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'


# Generic authorisation
LOGIN_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
