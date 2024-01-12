from django.views.generic import ListView, DetailView
from django.utils.translation import gettext_lazy as _

from .models import AircraftModel


# Create your views here.
class AircraftListView(ListView):
    model = AircraftModel
    template_name = 'user/apps/aircraft/aircrafts.html'
    context_object_name = 'aircrafts'
    extra_context = {
        'title': _('Aircrafts'),
        'subtitle': _('List of all AirERP aircrafts')
    }


class AircraftDetailView(DetailView):
    model = AircraftModel
    template_name = 'user/apps/aircraft/aircraft.html'
    context_object_name = 'aircraft'
    extra_context = {
        'title': _('Aircraft'),
        'subtitle': _('Detail information about aircraft')
    }
