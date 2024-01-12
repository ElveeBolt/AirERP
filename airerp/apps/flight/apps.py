from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlightConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.flight'
    verbose_name = _('Flight')
