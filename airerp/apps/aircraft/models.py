from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class AircraftModel(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Model name'))
    description = models.TextField(verbose_name=_('Description'))
    manufacturer = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Manufacturer'))
    manufacturer_year = models.IntegerField(null=False, blank=False, verbose_name=_('Manufacturer year'))
    image = models.ImageField(upload_to='aircraft', null=True, blank=True, verbose_name=_('Image'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('model')
        verbose_name_plural = _('Aircraft Models')


class Aircraft(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Name'))
    model = models.ForeignKey(AircraftModel, on_delete=models.CASCADE, verbose_name=_('Aircraft Model'))
    total_seats = models.PositiveIntegerField(default=0, verbose_name=_('Total seats'))
    window_seats = models.PositiveIntegerField(default=0, verbose_name=_('Window seats'))
    extra_legroom_seats = models.PositiveIntegerField(default=0, verbose_name=_('Extra legroom'))
    aisle_seats = models.PositiveIntegerField(default=0, verbose_name=_('Aisle seat'))

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        total_seat_types = self.window_seats + self.extra_legroom_seats + self.aisle_seats
        if total_seat_types > self.total_seats:
            raise ValidationError(
                _('The sum of window, extra legroom, and aisle seats cannot exceed the total seats in the aircraft.')
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('aircrafts')
        verbose_name_plural = _('Aircraft')
