'''Shorty Models'''
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import string
import random


RANDOM_SLUG_CHOICES = string.ascii_letters + string.digits + '_-'


def random_slug():
    while True:
        slug = ''.join(random.choice(RANDOM_SLUG_CHOICES) for _ in range(7))
        try:
            ShortURL.objects.get(path=slug)
        except ShortURL.DoesNotExist:
            return slug


class ShortURL(models.Model):
    path = models.SlugField(unique=True, error_messages={'unique': 'This short URL is already in use; please choose something different, or leave blank for a random URL',})
    redirect = models.URLField()
    user = models.ForeignKey(User, related_name='short_urls')
    created = models.DateTimeField(auto_now_add=True)
    external = models.BooleanField(default=False, help_text='Should this short link be available outside the company\'s network?')

    class Meta:
        ordering = ('-created', )
        verbose_name = 'Short URL'
        verbose_name_plural = 'Short URLs'

    def __unicode__(self):
        return '{}: {}'.format(self.path, self.redirect)

    def save(self, *args, **kwargs):
        if not self.path:
            self.path = random_slug()
        return super(ShortURL, self).save(*args, **kwargs)

    def build_uri(self, request):
        return request.build_absolute_uri(reverse('redirect', kwargs={'slug': self.path}))
