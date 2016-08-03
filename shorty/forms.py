'''Shorty Forms'''
from django import forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from .models import ShortURL
from .app_settings import EXTERNAL_FLAG


class ShortURLForm(forms.ModelForm):

    RESTRICTED_PATHS = (
        'admin',
    )

    redirect = forms.URLField(required=True, widget=forms.URLInput(attrs={'placeholder': 'Enter a URL'}))
    path = forms.SlugField(required=False, widget=forms.TextInput(attrs={'placeholder': 'short-url'}))
    override_existing = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, request, *args, **kwargs):
        self.request = request
        return super(ShortURLForm, self).__init__(*args, **kwargs)

    def clean_path(self):
        path = self.cleaned_data['path']

        if path in self.RESTRICTED_PATHS:
            raise forms.ValidationError('You cannot use that path. Please specify another.')

        return path

    def clean(self):
        cleaned_data = super(ShortURLForm, self).clean()
        redirect = cleaned_data.get('redirect')
        override_existing = cleaned_data.get('override_existing')

        if override_existing != '1' and redirect:
            short_urls = ShortURL.objects.filter(redirect=redirect)
            if short_urls:
                self.data = self.data.copy()
                self.data['override_existing'] = 1
                self.request.previous_short_urls = short_urls
                raise forms.ValidationError('That URL has been shortened previously.')

        return cleaned_data

    class Meta:
        model = ShortURL
        fields = ['redirect', 'path']
        if EXTERNAL_FLAG:
            fields.append('external')
