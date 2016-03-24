'''Shorty App Settings'''
from django.conf import settings


ADMIN_ENABLED = getattr(settings, 'SHORTY_ADMIN_ENABLED', True)
