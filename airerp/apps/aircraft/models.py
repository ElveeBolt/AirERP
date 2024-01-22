from cloudinary.models import CloudinaryField
from cloudinary.utils import cloudinary_url
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.airport.models import Airport


# Create your models here.
class AircraftManufacturerModel(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('title'))
    image = CloudinaryField('aircraft/manufacturer', null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True, verbose_name=_('Description'))

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _('manufacturers')
        verbose_name_plural = _('Manufacturer')


class AircraftModel(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Model title'))
    description = models.TextField(verbose_name=_('Description'))
    manufacturer = models.ForeignKey(AircraftManufacturerModel, on_delete=models.CASCADE, verbose_name=_('Manufacturer'))
    manufacturer_year = models.IntegerField(null=False, blank=False, verbose_name=_('Manufacturer year'))
    image = CloudinaryField('aircraft', null=True, blank=True, max_length=255)
    thumbnail = CloudinaryField('aircraft', null=True, blank=True, max_length=255)

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img_public_id = self.image.public_id
            img_url, options = cloudinary_url(
                img_public_id,
                format="jpg",
                crop="fill",
                width=1280,
                height=720
            )
            self.thumbnail = img_url
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('model')
        verbose_name_plural = _('Aircraft Models')


class Aircraft(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Name'))
    model = models.ForeignKey(AircraftModel, on_delete=models.CASCADE, verbose_name=_('Aircraft Model'))
    current_airport = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, blank=True)
    total_seats = models.PositiveIntegerField(default=0, verbose_name=_('Total seats'))
    window_seats = models.PositiveIntegerField(default=0, verbose_name=_('Window seats'))
    extra_legroom_seats = models.PositiveIntegerField(default=0, verbose_name=_('Extra legroom'))
    aisle_seats = models.PositiveIntegerField(default=0, verbose_name=_('Aisle seat'))

    def __str__(self):
        return f"{self.title}"

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
