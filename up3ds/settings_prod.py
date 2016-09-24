from .settings import *

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = '/var/www/media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}
