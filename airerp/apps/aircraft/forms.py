from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, Row, Column, ButtonHolder
from .models import Aircraft, AircraftModel, AircraftManufacturerModel


class AircraftManagerForm(forms.ModelForm):
    class Meta:
        model = Aircraft
        fields = ['title', 'model', 'current_airport', 'total_seats', 'window_seats', 'extra_legroom_seats', 'aisle_seats']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Column('title', 'model', 'current_airport', 'total_seats'),
            Fieldset(
                _('Seats informations'),
                Row('window_seats', 'extra_legroom_seats', 'aisle_seats', css_class='grid grid-cols-3 gap-4 mb-4')
            ),
            ButtonHolder(
                Submit('Save', 'Save', css_class='btn btn-primary'),
            ),
        )


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
