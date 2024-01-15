from django import forms
from django.utils.translation import gettext_lazy as _

from .models import City, Airport


class CityManagerForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('City...')}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Country...')}),
        }
        

class AirportManagerForm(forms.ModelForm):
    class Meta:
        model = Airport
        fields = ['code', 'name', 'city', 'latitude', 'longitude']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Code...')}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Airport name...')}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': _('Latitude...')}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': _('Longitude...')}),
        }