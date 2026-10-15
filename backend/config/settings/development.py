from .base import * 
import os
from pathlib import Path
from dotenv import load_dotenv

DEBUG = True


BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / "media"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.getenv("DB_NAME", str(BASE_DIR / "db.sqlite3")),
        'USER': os.getenv("DB_USER", ""),
        'PASSWORD': os.getenv("DB_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", ""),
        'PORT': os.getenv("DB_PORT", ""),
    }
}

if DATABASES['default']['ENGINE'] == "django.db.backends.sqlite3":
    database_name = Path(DATABASES['default']['NAME'])
    if not database_name.is_absolute():
        DATABASES['default']['NAME'] = str(BASE_DIR / database_name)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PORT = 465
EMAIL_HOST_USER = os.getenv('ACCOUNT')
EMAIL_HOST_PASSWORD = os.getenv('PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
