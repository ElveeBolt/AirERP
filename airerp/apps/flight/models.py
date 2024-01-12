from django.db import models
from apps.service.models import Service, Baggage
from apps.airport.models import Airport
from apps.aircraft.models import Aircraft, Seat
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Flight(models.Model):
    code = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Code'))
    departure_from = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_from', verbose_name=_('Departure from'))
    arrival_to = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_to', verbose_name=_('Arrival to'))
    departure_time = models.DateTimeField(null=False, blank=False, verbose_name=_('Departure datetime'))
    arrival_time = models.DateTimeField(null=False, blank=False, verbose_name=_('Arrival datetime'))
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, verbose_name=_('Aircraft'))
    base_price = models.PositiveIntegerField(default=0, verbose_name=_('Base price ($)'))
    baggage = models.ForeignKey(Baggage, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Baggage'))
    baggage_price = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_('Baggage price ($)'))
    first_class_surcharge = models.PositiveIntegerField(default=0, verbose_name=_('First class price surcharge'))
    business_class_surcharge = models.PositiveIntegerField(default=0, verbose_name=_('Business class price surcharge'))
    economy_class_surcharge = models.PositiveIntegerField(default=0, verbose_name=_('Economy class price surcharge'))

    def __str__(self):
        return f"{self.code}"

    class Meta:
        verbose_name = _('flights')
        verbose_name_plural = _('Flight')


class FlightService(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name=_('Flight'))
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_('Service'))
    price = models.IntegerField(verbose_name=_('Price ($)'))

    def __str__(self):
        return f"{self.flight}, {self.service}"

    class Meta:
        verbose_name = _('services')
        verbose_name_plural = _('Flight service')


class FlightSeat(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name=_('Flight'))
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, verbose_name=_('Seat'))
    price = models.IntegerField(verbose_name=_('Price ($)'))

    def __str__(self):
        return f"{self.seat} - {self.price}$"

    class Meta:
        verbose_name = _('seats')
        verbose_name_plural = _('Flight seat')