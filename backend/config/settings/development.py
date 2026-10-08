from .base import * 

DEBUG = True
SECRET_KEY = 'development-key'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}