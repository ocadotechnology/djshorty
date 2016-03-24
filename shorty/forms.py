'''Shorty Forms'''
from django import forms

from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    redirect = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter a URL'}))
    path = forms.URLField(required=False, widget=forms.URLInput(attrs={'placeholder': 'short-url'}))

    class Meta:
        model = ShortURL
        fields = ['redirect', 'path']
