from datetime import date

import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.airport.models import Airport
from .models import Flight


class FlightFilter(django_filters.FilterSet):
    departure_from = django_filters.ModelChoiceFilter(
        queryset=Airport.objects.all(),
        label=_('Departure from:'),
        empty_label=_('Select from'),
        required=True,
        widget=forms.Select(attrs={
            'placeholder': 'Select from...',
            'class': 'form-control'
        })
    )
    arrival_to = django_filters.ModelChoiceFilter(
        queryset=Airport.objects.all(),
        label=_('Arrival to:'),
        empty_label=_('Select to'),
        required=True,
        widget=forms.Select(attrs={
            'placeholder': 'Select to...',
            'class': 'form-control'
        })
    )
    departure_time = django_filters.DateFilter(
        label=_('Departure date:'),
        lookup_expr='date',
        widget=forms.DateInput(attrs={
            'placeholder': 'Select date...',
            'class': 'form-control',
            'type': 'date',
            'min': str(date.today())
        }),
        required=True
    )
    seat_class = django_filters.ChoiceFilter(
        choices=Flight.CLASS_CHOICES,
        label=_('Seat class:'),
        widget=forms.Select(attrs={
            'placeholder': _('Select seat class...'),
            'class': 'form-control'
        }),
    )

    class Meta:
        model = Flight
        fields = ['departure_from', 'arrival_to', 'departure_time', 'seat_class']