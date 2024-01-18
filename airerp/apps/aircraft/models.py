import os
import sys
from io import BytesIO

from PIL import Image
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class AircraftModel(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Model name'))
    description = models.TextField(verbose_name=_('Description'))
    manufacturer = models.CharField(null=False, blank=False, max_length=255, verbose_name=_('Manufacturer'))
    manufacturer_year = models.IntegerField(null=False, blank=False, verbose_name=_('Manufacturer year'))
    image = CloudinaryField('aircraft', null=True, blank=True, max_length=255)
    thumbnail = CloudinaryField('aircraft/thumbnails')

    def __str__(self):
        return f"{self.name}"

    def save(self, **kwargs):
        width = 1280
        height = 720

        output_size = (width, height)
        output_thumb = BytesIO()

        img = Image.open(self.image)
        img_name = os.path.splitext(self.image.name)[0]

        if img.height > height or img.width > width:
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            img.save(output_thumb, format=img.format, quality=90)

        self.thumbnail = InMemoryUploadedFile(
            file=output_thumb,
            field_name='ImageField',
            name=f"{img_name}_thumb.{img.format}",
            content_type='image/jpeg',
            size=sys.getsizeof(output_thumb),
            charset=None
        )
        super().save()

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
