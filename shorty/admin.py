'''Shorty Admin'''

from .models import ShortURL
from django.contrib import admin

admin.site.register(ShortURL, admin.ModelAdmin)
