from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Service, Baggage


class ServiceManagerForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'icon', 'max_quantity']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Service name...')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Description...')}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Icon...')}),
            'max_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Max quantity...')}),
        }


class BaggageManagerForm(forms.ModelForm):
    class Meta:
        model = Baggage
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Baggage name...')}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': _('Description...')}),
        }
