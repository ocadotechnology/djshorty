'''Shorty Admin'''

from .models import ShortURL
from django.contrib import admin

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('path', 'redirect', 'user', 'external',)
    search_fields = ('path', 'redirect', 'user__username',)
    list_filter = ('external',)

admin.site.register(ShortURL, ShortURLAdmin)
