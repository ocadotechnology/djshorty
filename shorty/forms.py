'''Shorty Forms'''
from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import ShortURL
from .app_settings import EXTERNAL_FLAG


class ShortURLForm(forms.ModelForm):
    redirect = forms.URLField(required=True, widget=forms.URLInput(attrs={'placeholder': 'Enter a URL'}))
    path = forms.SlugField(required=False, widget=forms.TextInput(attrs={'placeholder': 'short-url'}))
    override_existing = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        return super(ShortURLForm, self).__init__(*args, **kwargs)

    def clean_override_existing(self):
        redirect = self.cleaned_data['redirect']
        override_existing = self.cleaned_data['override_existing']

        if override_existing != '1':
            short_urls = ShortURL.objects.filter(redirect=redirect)
            if short_urls:
                self.request.previous_short_urls = short_urls
                raise forms.ValidationError('That URL has been shortened previously.')

        return override_existing

    class Meta:
        model = ShortURL
        fields = ['redirect', 'path']
        if EXTERNAL_FLAG:
            fields.append('external')
