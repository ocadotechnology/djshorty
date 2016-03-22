'''Django settings for example_project project.'''
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dbfile'),  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media/media')

MEDIA_URL = '/static/media/'

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), 'media'),
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'NOT-A-SECRET'

ROOT_URLCONF = 'django_autoconfig.autourlconf'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'example_project.wsgi.application'

INSTALLED_APPS = (
    'shorty',
)

LOGIN_URL = 'admin:login'
LOGOUT_URL = 'admin:logout'

try:
    from example_project.local_settings import *
except ImportError:
    pass

from django_autoconfig import autoconfig
autoconfig.configure_settings(globals())
