from datetime import datetime

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Flight, FlightService


class FlightManagerForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['code', 'departure_from', 'arrival_to', 'departure_time', 'arrival_time', 'aircraft', 'base_price', 'baggage', 'baggage_price', 'seat_class', 'window_seat_price', 'extra_legroom_seat_price', 'aisle_seat_price']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Code...')}),
            'departure_from': forms.Select(attrs={'class': 'form-control'}),
            'arrival_to': forms.Select(attrs={'class': 'form-control'}),
            'departure_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': str(datetime.now())}),
            'arrival_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'min': str(datetime.now())}),
            'aircraft': forms.Select(attrs={'class': 'form-control'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'baggage': forms.Select(attrs={'class': 'form-control'}),
            'baggage_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'seat_class': forms.Select(attrs={'class': 'form-control'}),
            'window_seat_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'extra_legroom_seat_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'aisle_seat_price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_time = cleaned_data.get("departure_time")
        arrival_time = cleaned_data.get("arrival_time")

        if departure_time > arrival_time:
            raise forms.ValidationError(_("The arrival date cannot be earlier than the departure date."))

        return cleaned_data


class FlightServiceManagerForm(forms.ModelForm):
    class Meta:
        model = FlightService
        fields = ['flight', 'service', 'price']
        widgets = {
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }