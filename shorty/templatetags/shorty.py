'''Shorty Template Tags'''
from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def build_short_url(context, path):
    return context['request'].build_absolute_uri(reverse('redirect', kwargs={'slug': path}))
