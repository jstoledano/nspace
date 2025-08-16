__author__ = 'Javier Sanchez'
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG



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