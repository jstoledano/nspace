"""
Django settings for namespace project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize django-environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# The .env file should be in the src/ directory (which is BASE_DIR)
environ.Env.read_env(BASE_DIR / '.env')


MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = '/assets/'
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "assets",
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ],
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


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c_@a3lqj$4xn_+gltjcp4*nj5*8@zqdj750t-bu##yeau1f5p_'


SITE_ID = 1
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': env.db(),
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'taggit_templatetags',

    'core',
    'blog',

    'taggit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'namespace.urls'
WSGI_APPLICATION = 'namespace.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = True
USE_TZ = True

BITLY_LOGIN = env('BITLY_LOGIN', default='')
BITLY_API_KEY = env('BITLY_API_KEY', default='')


