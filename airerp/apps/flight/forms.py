from datetime import datetime

from django import forms
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Flight, FlightService


class FlightManagerForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['code', 'departure_from', 'arrival_to', 'departure_time', 'arrival_time', 'aircraft', 'base_price', 'baggage', 'baggage_price', 'seat_class', 'window_seat_price', 'extra_legroom_seat_price', 'aisle_seat_price', 'status']
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
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        departure_time = cleaned_data.get("departure_time")
        arrival_time = cleaned_data.get("arrival_time")
        departure_from = cleaned_data.get("departure_from")
        aircraft = cleaned_data.get("aircraft")
        status = cleaned_data.get("status")

        if departure_time > arrival_time:
            raise forms.ValidationError(_("The arrival date cannot be earlier than the departure date."))

        self.validate_aircraft_availability(
            status=status,
            aircraft=aircraft,
            departure_time=departure_time,
            departure_from=departure_from,
            arrival_time=arrival_time
        )

        return cleaned_data

    def validate_aircraft_availability(self, status, aircraft, departure_time, departure_from, arrival_time):
        if status == 'C' and arrival_time > timezone.now():
            raise forms.ValidationError(_("The arrival time cannot be earlier than the current date and time when the flight is marked as completed."))

        if aircraft.current_airport != departure_from:
            raise forms.ValidationError(_("There is no aircraft at the departure airport."))

        other_flights = Flight.objects.filter(
            Q(aircraft=aircraft),
            ~Q(pk=self.instance.pk),
            Q(departure_time__lt=arrival_time) & Q(arrival_time__gt=departure_time)
        )

        if other_flights.exists():
            raise forms.ValidationError(_("This aircraft already has a scheduled flight after the selected departure time."))


class FlightServiceManagerForm(forms.ModelForm):
    class Meta:
        model = FlightService
        fields = ['flight', 'service', 'price']
        widgets = {
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }