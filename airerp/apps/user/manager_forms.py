from datetime import date, timedelta

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.ticket.forms import Ticket

from apps.ticket.forms import BaggageRadioSelect, SeatRadioSelect


class OnboardingForm(forms.ModelForm):
    ONBOARDING_CHOICES = (
        (True, _('Is onboarding')),
        (False, _('Is not onboarding'))
    )

    is_onboarding = forms.ChoiceField(
        choices=ONBOARDING_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Ticket
        fields = ('is_onboarding',)


class CheckinForm(forms.ModelForm):
    CHECKIN_CHOICES = (
        (True, _('Is checkin')),
        (False, _('Is not checkin'))
    )

    is_checkin = forms.ChoiceField(
        choices=CHECKIN_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Ticket
        exclude = ('code', 'flight', 'user', 'is_onboarding')

        widgets = {
            'gender': forms.Select(
                attrs={
                    'placeholder': _('Gender...'),
                    'class': 'form-control'
                },
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': _('First name...'),
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': _('Last name...'),
                    'class': 'form-control',
                }
            ),
            'date_birth': forms.DateInput(
                attrs={
                    'placeholder': _('Date birth...'),
                    'class': 'form-control',
                    'type': 'date',
                    'max': str(date.today() - timedelta(days=365 * 18))
                }
            ),
            'citizenship': forms.TextInput(
                attrs={
                    'placeholder': _('Citizenship...'),
                    'class': 'form-control',
                }
            ),
            'document_type': forms.Select(
                attrs={
                    'placeholder': _('Document type...'),
                    'class': 'form-control'
                },
            ),
            'document_serial': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'document_date_expiry': forms.DateInput(
                attrs={
                    'placeholder': _('Date expiry...'),
                    'class': 'form-control',
                    'type': 'date',
                    'min': str(date.today())
                }
            ),
            'baggage': BaggageRadioSelect(),
            'seat': SeatRadioSelect()
        }

        help_texts = {
            'date_birth': _('You must be older than 18 years')
        }

    def __init__(self, flight=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight = flight

        if flight:
            self.fields['baggage'].widget.choices = [
                (False, mark_safe(
                    f'<div class="w-20"><img src="/static/images/baggage_icon_false.svg" class="mx-auto"></div><div class="flex-1"><div class="text-black font-semibold">No</div><div class="text-sm">Without additional baggage</div></div>')),
                (True, mark_safe(
                    f'<div class="w-20"><img src="/static/images/baggage_icon_true.svg" class="mx-auto"></div><div class="flex-1"><div class="text-black font-semibold">Yes</div><div class="text-sm">{self.flight.baggage}</div></div><div class="price font-bold text-green-500 bg-gray-50 px-3 py-2 rounded-xl" data_price="{self.flight.baggage_price}">+{self.flight.baggage_price}$</div>')),
            ]

            # available_seats = FlightSeat.objects.filter(flight=self.flight)
            # seat_choices = [
            #     (
            #         flight_seat.pk,
            #         mark_safe(
            #             f'<div class="w-20"><img src="{flight_seat.seat.image.url}" class="mx-auto"></div><div class="flex-1"><div class="text-black font-semibold">{flight_seat.seat.name}</div><div class="text-sm">{flight_seat.seat.description}</div></div><div class="font-bold text-green-500 bg-gray-50 px-3 py-2 rounded-xl">+{flight_seat.price}$</div>')
            #     ) for flight_seat in available_seats
            # ]
            #
            # self.fields['seat'].widget.choices = seat_choices