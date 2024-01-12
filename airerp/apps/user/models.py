from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name=_('Email'))

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.username
