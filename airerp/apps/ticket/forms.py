from datetime import date, timedelta

from django import forms
from django.forms import inlineformset_factory
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Ticket, TicketService


class BaggageRadioSelect(forms.RadioSelect):
    template_name = 'user/widgets/radio_baggage.html'
    option_template_name = 'user/widgets/radio_baggage_option.html'


class SeatRadioSelect(forms.RadioSelect):
    template_name = 'user/widgets/radio_seat.html'
    option_template_name = 'user/widgets/radio_seat_option.html'


class ServiceNumberInput(forms.NumberInput):
    template_name = 'user/widgets/number_service.html'


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('code', 'flight', 'user')

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
            'seat_type': forms.Select(
                attrs={
                    'placeholder': _('Seat type...'),
                    'class': 'form-control'
                },
            ),
        }

        help_texts = {
            'date_birth': _('You must be older than 18 years')
        }

    def __init__(self, flight=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flight = flight

        if self.flight:
            self.fields['baggage'].widget.choices = [
                (False, mark_safe(
                    f'<div class="w-20"><img src="/static/images/baggage_icon_false.svg" class="mx-auto"></div><div class="flex-1"><div class="text-black font-semibold">No</div><div class="text-sm">Without additional baggage</div></div>')),
                (True, mark_safe(
                    f'<div class="w-20"><img src="/static/images/baggage_icon_true.svg" class="mx-auto"></div><div class="flex-1"><div class="text-black font-semibold">Yes</div><div class="text-sm">{self.flight.baggage}</div></div><div class="price font-bold text-green-500 bg-gray-50 px-3 py-2 rounded-xl" data_price="{self.flight.baggage_price}">+{self.flight.baggage_price}$</div>')),
            ]

            available_seat_types = flight.get_available_seat_types()
            self.fields['seat_type'].choices = [(key, value) for key, value in available_seat_types.items()]


class TicketServiceForm(forms.ModelForm):
    class Meta:
        model = TicketService
        fields = ('quantity', 'service')
        widgets = {
            'service': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        flight_service = self.initial.get('service')

        if flight_service:
            self.fields['quantity'].help_text = mark_safe(f'<div class="text-3xl"><i class="{flight_service.service.icon}"></i></div><div><div class="text-black font-semibold">{flight_service.service.name}</div><div class="text-sm">{flight_service.service.description}</div></div><div class="font-bold text-green-500 bg-gray-50 px-3 py-2 rounded-xl">+{flight_service.price}$</div>')
            self.fields['quantity'].widget = ServiceNumberInput()
            self.fields['quantity'].widget.attrs = {
                'class': 'form-control',
                'min': 0,
                'max': flight_service.service.max_quantity
            }


TicketServiceFormSet = inlineformset_factory(Ticket, TicketService, form=TicketServiceForm, extra=0)


class TicketManagerForm(forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ['user', 'is_checkin', 'is_onboarding']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'flight': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'citizenship': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'document_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'document_date_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'baggage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'seat_type': forms.Select(attrs={'class': 'form-control'}),
        }


class TicketServiceManagerForm(forms.ModelForm):
    class Meta:
        model = TicketService
        fields = ('quantity', 'service')

    def __init__(self, services=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.services = services

        choices = [(service.id, service) for service in self.services]
        self.fields['service'].widget = forms.Select(choices=choices)


class TicketCheckinManagerForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('is_checkin', 'seat_number')
        widgets = {
            'is_checkin': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'seat_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_checkin = cleaned_data.get('is_checkin')
        seat_number = cleaned_data.get('seat_number')

        if is_checkin and not seat_number:
            raise forms.ValidationError(_('Please add seat number'))

        if is_checkin and seat_number:
            is_seat_taken = Ticket.objects.filter(flight=self.instance.flight, seat_number=seat_number, is_checkin=True).exists()
            if is_seat_taken:
                raise forms.ValidationError(_('The seat is already taken.'))

        return cleaned_data


class TicketOnboardingManagerForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('is_onboarding', )
        widgets = {
            'is_onboarding': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }