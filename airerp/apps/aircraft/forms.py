from django import forms
from .models import Aircraft, AircraftModel, AircraftManufacturerModel


class AircraftManagerForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ['title', 'model', 'total_seats', 'window_seats', 'extra_legroom_seats', 'aisle_seats']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.Select(attrs={'class': 'form-control'}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'window_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_legroom_seats': forms.NumberInput(attrs={'class': 'form-control'}),
            'aisle_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AircraftModelManagerForm(forms.ModelForm):
    class Meta:
        model = AircraftModel
        fields = ['title', 'description', 'manufacturer', 'manufacturer_year', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class AircraftManufacturerManagerForm(forms.ModelForm):
    class Meta:
        model = AircraftManufacturerModel
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
