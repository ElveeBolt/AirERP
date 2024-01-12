from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class City(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name=_('City'))
    country = models.CharField(unique=True, null=False, blank=False, max_length=100, verbose_name=_('Country'))

    def __str__(self):
        return f"{self.name}, {self.country}"

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('Cities')


class Airport(models.Model):
    code = models.CharField(unique=True, max_length=10, verbose_name=_('Code'))
    name = models.CharField(null=False, blank=False, max_length=100, verbose_name=_('Airport name'))
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_('City'))
    latitude = models.FloatField(null=False, blank=False, verbose_name=_('Airport latitude'))
    longitude = models.FloatField(null=False, blank=False, verbose_name=_('Airport longitude'))

    def __str__(self):
        return f"{self.code}, {self.name}"

    class Meta:
        verbose_name = _('airport')
        verbose_name_plural = _('Airports')
