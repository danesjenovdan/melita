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

ALLOWED_HOSTS = ["localhost", "melitaproject.eu"]
CSRF_TRUSTED_ORIGINS = ["https://melitaproject.eu/"]


ENABLE_S3 = os.getenv("DJANGO_ENABLE_S3", False)
# DJANGO STORAGE SETTINGS
if ENABLE_S3:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "access_key": os.getenv("DJANGO_AWS_ACCESS_KEY_ID", ""),
                "secret_key": os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY", ""),
                "bucket_name": os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME", ""),
                "region_name": os.getenv("AWS_REGION_NAME", "fr-par"),
                "endpoint_url": os.getenv(
                    "DJANGO_AWS_S3_ENDPOINT_URL", "https://s3.fr-par.scw.cloud"
                ),
                "location": os.getenv("DJANGO_AWS_LOCATION", "storyteller"),
                "file_overwrite": os.getenv("AWS_S3_FILE_OVERWRITE", False),
                "signature_version": os.getenv("DJANGO_AWS_S3_SIGNATURE_VERSION", "s3v4"),
                "querystring_auth": os.getenv("AWS_QUERYSTRING_AUTH", False),
                "default_acl": os.getenv("AWS_DEFAULT_ACL", "public-read"),
            },
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"

try:
    from .local import *
except ImportError:
    pass
