import random
import string
from django.db.models import Sum
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.flight.models import Flight, FlightService
from apps.user.models import User


# Create your models here.
class Ticket(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    DOCUMENT_TYPE_CHOICES = (
        ('IP', 'International passport'),
    )

    SEAT_TYPE_CHOICES = (
        ('window', _('Window seat')),
        ('extra_legroom', _('Extra legroom seat')),
        ('aisle', _('Aisle seat')),
    )

    code = models.CharField(null=True, max_length=6, unique=True, verbose_name=_('Ticket code'))
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name=_('Flight'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    gender = models.CharField(max_length=1, default='M', choices=GENDER_CHOICES, verbose_name=_('Gender'))
    first_name = models.CharField(null=True, blank=False, max_length=255, verbose_name=_('First name'))
    last_name = models.CharField(null=True, blank=False, max_length=255, verbose_name=_('Last name'))
    date_birth = models.DateField(null=True, blank=False, verbose_name=_('Date birth'))
    citizenship = models.CharField(null=True, blank=False, max_length=255, verbose_name=_('Citizenship'))
    document_type = models.CharField(max_length=2, default='IP', choices=DOCUMENT_TYPE_CHOICES, verbose_name=_('Document type'))
    document_serial = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Document serial'))
    document_date_expiry = models.DateField(null=False, blank=False, verbose_name=_('Date document expiry'))
    baggage = models.BooleanField(default=False, verbose_name=_('Additional baggage'))
    seat_type = models.CharField(null=True, blank=True, max_length=100, choices=SEAT_TYPE_CHOICES, verbose_name=_('Seat type'))
    is_checkin = models.BooleanField(default=False, verbose_name=_('Is checkin'))
    is_onboarding = models.BooleanField(default=False, verbose_name=_('Is onboarding'))
    date_booked = models.DateTimeField(auto_now_add=True, verbose_name=_('Date booked'))

    def __str__(self):
        return f"{self.flight}"

    class Meta:
        verbose_name = _('tickets')
        verbose_name_plural = _('Ticket')

    def calculate_total_price(self):
        baggage_price = self.flight.baggage_price if self.baggage else 0
        additional_services_price = self.ticketservice_set.aggregate(total=Sum('service__price'))['total'] or 0

        match self.seat_type:
            case 'window':
                seat_price = self.flight.window_seat_price
            case 'extra_legroom':
                seat_price = self.flight.extra_legroom_seat_price
            case 'aisle':
                seat_price = self.flight.aisle_seat_price
            case _:
                seat_price = 0

        total_price = self.flight.base_price + baggage_price + seat_price + additional_services_price

        return total_price

    def save(self, *args, **kwargs):
        if not self.code:
            while True:
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Ticket.objects.filter(code=code).exists():
                    self.code = code
                    break

        return super().save(*args, **kwargs)


class TicketService(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name=_('Ticket'))
    service = models.ForeignKey(FlightService, on_delete=models.CASCADE, verbose_name=_('Service'))
    quantity = models.PositiveIntegerField(default=0, verbose_name=_('Quantity'))

    def __str__(self):
        return f"{self.ticket}, {self.service}"

    class Meta:
        verbose_name = _('services')
        verbose_name_plural = _('Ticket service')
