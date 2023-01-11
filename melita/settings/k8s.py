from .base import *

DEBUG = os.getenv("DJANGO_DEBUG", False)

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "changeme")

STATIC_ROOT = os.getenv("DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = os.getenv("DJANGO_STATIC_URL", "/static/")
MEDIA_ROOT = os.getenv("DJANGO_MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = os.getenv("DJANGO_MEDIA_URL", "/media/")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.getenv("DJANGO_DATABASE_HOST", "db"),
        "PORT": os.getenv("DJANGO_DATABASE_PORT", "5432"),
        "NAME": os.getenv("DJANGO_DATABASE_NAME", "wagtail"),
        "USER": os.getenv("DJANGO_DATABASE_USER", "wagtail"),
        "PASSWORD": os.getenv("DJANGO_DATABASE_PASSWORD", "changeme"),
    }
}

ALLOWED_HOSTS = ["localhost", "melita.lb.djnd.si"]
CSRF_TRUSTED_ORIGINS = ["https://melita.lb.djnd.si"]


try:
    from .local import *
except ImportError:
    pass
