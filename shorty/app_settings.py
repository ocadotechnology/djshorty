'''Shorty App Settings'''
from django.conf import settings


ADMIN_ENABLED = getattr(settings, 'SHORTY_ADMIN_ENABLED', True)

EXTERNAL_FLAG = getattr(settings, 'SHORTY_EXTERNAL_FLAG', False)

CANONICAL_DOMAIN = getattr(settings, 'SHORTY_CANONICAL_DOMAIN', None)
