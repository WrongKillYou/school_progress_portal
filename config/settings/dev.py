# config/settings/dev.py

from .base import *
from decouple import config

# Enable Debug Mode
DEBUG = True

# Allow local access
ALLOWED_HOSTS = ['*']  # Or ['localhost', '127.0.0.1']

# MySQL Database Configuration (override base if needed)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
