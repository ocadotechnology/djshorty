'''Shorty App Settings'''
from django.conf import settings

from .utils import is_external_request


ADMIN_ENABLED = getattr(settings, 'SHORTY_ADMIN_ENABLED', True)

EXTERNAL_FLAG = getattr(settings, 'SHORTY_EXTERNAL_FLAG', False)
IS_EXTERNAL_REQUEST_FUNC = getattr(settings, 'SHORT_IS_EXTERNAL_REQUEST_FUNC', is_external_request)
