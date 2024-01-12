from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class PromoCode(models.Model):
    code = models.CharField(unique=True, max_length=20, verbose_name=_('Code'))
    discount = models.IntegerField(null=False, blank=False, verbose_name=_('Discount'))
