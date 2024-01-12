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
    first_class_seats = models.PositiveIntegerField(default=0, verbose_name=_('First class seats'))
    business_class_seats = models.PositiveIntegerField(default=0, verbose_name=_('Business class seats'))
    economy_class_seats = models.PositiveIntegerField(default=0, verbose_name=_('Economy class seats'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('aircrafts')
        verbose_name_plural = _('Aircraft')


class Seat(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    image = models.ImageField(upload_to='seat', null=True, blank=True, verbose_name=_('Image'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('seats')
        verbose_name_plural = _('Seat')