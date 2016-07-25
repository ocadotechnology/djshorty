DEFAULT_SETTINGS = {
    'AUTOCONFIG_URL_PREFIXES': {
        'shorty': '',
    },
}

SETTINGS = {
    'INSTALLED_APPS': [
        'django.contrib.admin',
        'nuit',
    ],
    'NUIT_GLOBAL_TITLE': 'Shorty',
    'CSP_SCRIPT_SRC': (
        "'self'",
        "https://cdnjs.cloudflare.com/ajax/libs/clipboard.js/1.5.8/clipboard.min.js",
    ),
}
