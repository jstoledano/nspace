__author__ = 'Javier Sanchez'
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "namespace",
    "USER": "javier",
    "PASSWORD": "santo97",
    "HOST": "localhost",
    "PORT": "5432",
    }
}

INTERNAL_IPS = ("127.0.0.1",)

INSTALLED_APPS += ("debug_toolbar", )
INTERNAL_IPS = ("127.0.0.1",)
MIDDLEWARE_CLASSES += (
    # 'annoying.middlewares.StaticServe',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}