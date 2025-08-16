from .base import *

DEBUG=False
#DEBUG=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDER_PROTOCOL', 'https')

# ALLOWED_HOSTS is now managed via the .env file in base.py
INTERNAL_IPS = ("127.0.0.1",)



# Caching configuration is now managed via the .env file
CACHES = {
    'default': env.cache('CACHE_URL'),
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
