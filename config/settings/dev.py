from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']  # Or ['localhost', '127.0.0.1'] for stricter dev

# Example development database (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
