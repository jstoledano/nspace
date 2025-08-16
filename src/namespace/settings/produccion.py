from .base import *

DEBUG=False
#DEBUG=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDER_PROTOCOL', 'https')

ALLOWED_HOSTS = ['namespace.mx', '192.3.90.48', 'hydra.namespace.mx', 'www.namespace.mx', '127.0.0.1', 'localhost']
INTERNAL_IPS = ("127.0.0.1",)

DATABASES = {
    "default": {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "nspace",
    "USER": "javier",
    "PASSWORD": "s4p0dr1l0+N!",
    "HOST": "localhost",
    "PORT": "5432",
    }
}

CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "127.0.0.1:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            # "PASSWORD": "secretpassword", # Optional
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
