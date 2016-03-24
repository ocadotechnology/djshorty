'''Shorty Forms'''
from django import forms

from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    redirect = forms.URLField(required=True, widget=forms.URLInput(attrs={'placeholder': 'Enter a URL'}))
    path = forms.SlugField(required=False, widget=forms.TextInput(attrs={'placeholder': 'short-url'}))

    class Meta:
        model = ShortURL
        fields = ['redirect', 'path']
