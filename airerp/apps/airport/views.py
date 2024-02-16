from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DeleteView, UpdateView, CreateView
from apps.user.mixins import SupervisorManagerMixin

from .forms import AirportManagerForm, CityManagerForm
from .models import Airport, City


# Create your views here.
class AirportManagerListView(SupervisorManagerMixin, ListView):
    model = Airport
    template_name = 'manager/apps/airport/airports.html'
    context_object_name = 'airports'
    extra_context = {
        'title': _('Airports'),
        'subtitle': _('List of all AirERP airports')
    }


class AirportManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
    model = Airport
    form_class = AirportManagerForm
    template_name = 'manager/apps/airport/airport.html'
    context_object_name = 'airport'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-airports')
    extra_context = {
        'title': _('Airport'),
        'subtitle': _('Detail information about airport')
    }


class AirportManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = Airport
    success_url = reverse_lazy('manager-airports')
    success_message = _('Delete object is successful')


class AirportManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = Airport
    form_class = AirportManagerForm
    template_name = 'manager/apps/airport/airport.html'
    success_url = reverse_lazy('manager-airports')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create airport'),
        'subtitle': _('Detail information about airport')
    }


class CityManagerListView(SupervisorManagerMixin, ListView):
    model = City
    template_name = 'manager/apps/airport/cities.html'
    context_object_name = 'cities'
    extra_context = {
        'title': _('Cities'),
        'subtitle': _('List of all AirERP cities')
    }


class CityManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityManagerForm
    template_name = 'manager/apps/airport/city.html'
    context_object_name = 'city'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-airport-cities')
    extra_context = {
        'title': _('City'),
        'subtitle': _('Detail information about city')
    }


class CityManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = City
    success_url = reverse_lazy('manager-airport-cities')
    success_message = _('Delete object is successful')


class CityManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = City
    form_class = CityManagerForm
    template_name = 'manager/apps/airport/city.html'
    success_url = reverse_lazy('manager-airport-cities')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create city'),
        'subtitle': _('Detail information about city')
    }