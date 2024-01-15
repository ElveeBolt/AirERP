from django import forms
from .models import Aircraft, AircraftModel


class AircraftManagerForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ['name', 'model', 'total_seats', 'window_seats', 'extra_legroom_seats', 'aisle_seats']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'window_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_legroom_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'aisle_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }