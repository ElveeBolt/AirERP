from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from apps.service.models import Service, Baggage
from apps.airport.models import Airport
from apps.aircraft.models import Aircraft
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Flight(models.Model):
    CLASS_CHOICES = (
        ('E', _('Economy Class')),
        ('PE', _('Premium Economy')),
        ('B', _('Business Class')),
        ('F', _('First Class')),
    )

    code = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Code'))
    departure_from = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_from', verbose_name=_('Departure from'))
    arrival_to = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_to', verbose_name=_('Arrival to'))
    departure_time = models.DateTimeField(null=False, blank=False, verbose_name=_('Departure datetime'))
    arrival_time = models.DateTimeField(null=False, blank=False, verbose_name=_('Arrival datetime'))
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, verbose_name=_('Aircraft'))
    base_price = models.PositiveIntegerField(default=0, verbose_name=_('Base price ($)'))
    baggage = models.ForeignKey(Baggage, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('Baggage'))
    baggage_price = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_('Baggage price ($)'))
    seat_class = models.CharField(null=False, blank=False, max_length=2, default='E', choices=CLASS_CHOICES, verbose_name=_('Seat Class'))
    window_seat_price = models.PositiveIntegerField(default=0, verbose_name=_('Window seat price ($)'))
    extra_legroom_seat_price = models.PositiveIntegerField(default=0, verbose_name=_('Extra legroom seat price ($)'))
    aisle_seat_price = models.PositiveIntegerField(default=0, verbose_name=_('Aisle seat price ($)'))

    free_window_seats = models.PositiveIntegerField(default=0)
    free_extra_legroom_seats = models.PositiveIntegerField(default=0)
    free_aisle_seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.code}"

    def get_free_seats(self):
        Ticket = apps.get_model('ticket', 'Ticket')
        free_seats = self.aircraft.total_seats - Ticket.objects.filter(flight=self).count()
        return free_seats

    def update_seat_availability(self):
        Ticket = apps.get_model('ticket', 'Ticket')
        self.free_window_seats = self.aircraft.window_seats - Ticket.objects.filter(flight=self, seat_type='window').count()
        self.free_extra_legroom_seats = self.aircraft.extra_legroom_seats - Ticket.objects.filter(flight=self, seat_type='extra_legroom').count()
        self.free_aisle_seats = self.aircraft.aisle_seats - Ticket.objects.filter(flight=self, seat_type='aisle').count()
        self.save()

    def get_available_seat_types(self):
        available_seat_types = {'': _('Random')}
        if self.free_window_seats > 0:
            available_seat_types['window'] = _(f'Window seat +{self.window_seat_price}$')
        if self.free_extra_legroom_seats > 0:
            available_seat_types['extra_legroom'] = _(f'Extra legroom seat +{self.extra_legroom_seat_price}$')
        if self.free_aisle_seats > 0:
            available_seat_types['aisle'] = _(f'Aisle seat +{self.aisle_seat_price}$')
        return available_seat_types

    def flight_duration(self):
        if self.departure_time and self.arrival_time:
            duration = self.arrival_time - self.departure_time
            return duration
        else:
            return None

    def clean(self):
        if self.departure_from == self.arrival_to:
            raise ValidationError(
                _('Departure and arrival airports must be different.')
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

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
