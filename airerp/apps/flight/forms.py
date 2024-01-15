from datetime import date
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Flight


class FlightSearchForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['departure_from', 'arrival_to', 'seat_class', 'departure_time']

        widgets = {
            'departure_from': forms.Select(
                attrs={
                    'placeholder': _('Departure from...'),
                    'class': 'form-control'
                },
            ),
            'arrival_to': forms.Select(
                attrs={
                    'placeholder': _('Arrival to...'),
                    'class': 'form-control'
                }
            ),
            'seat_class': forms.Select(
                attrs={
                    'placeholder': _('Seat class...'),
                    'class': 'form-control'
                }
            ),
            'departure_time': forms.DateInput(
                attrs={
                    'placeholder': _('Departure time...'),
                    'class': 'form-control',
                    'type': 'date',
                    'min': str(date.today())
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure_from'].empty_label = _('Departure from...')
        self.fields['arrival_to'].empty_label = _('Arrival to...')
