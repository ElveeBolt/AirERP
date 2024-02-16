import django_filters
from django import forms
from .models import AircraftModel, AircraftManufacturerModel
from django.utils.translation import gettext_lazy as _


class AircraftFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label=_('Title:'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter title...'),
            'class': 'form-control'
        })
    )
    manufacturer = django_filters.ModelChoiceFilter(
        queryset=AircraftManufacturerModel.objects.all(),
        field_name='manufacturer__title',
        label=_('Manufacturer:'),
        empty_label=_('Select manufacturer'),
        widget=forms.Select(attrs={
            'placeholder': 'Select manufacturer...',
            'class': 'form-control'
        })
    )

    class Meta:
        model = AircraftModel
        fields = ['title', 'manufacturer']