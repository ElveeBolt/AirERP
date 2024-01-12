from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Service(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Service name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))
    icon = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Icon'))
    max_quantity = models.PositiveIntegerField(null=False, blank=False, verbose_name=_('Max quantity'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('services')
        verbose_name_plural = _('Service')


class Baggage(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Baggage name'))
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _('baggages')
        verbose_name_plural = _('Baggage')