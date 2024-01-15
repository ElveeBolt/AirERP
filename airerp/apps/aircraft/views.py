from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.utils.translation import gettext_lazy as _

from .models import AircraftModel, Aircraft
from .forms import AircraftManagerForm


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


# Views for managers.
class AircraftManagerListView(ListView):
    model = Aircraft
    template_name = 'manager/apps/aircraft/aircrafts.html'
    context_object_name = 'aircrafts'
    extra_context = {
        'title': _('Aircrafts'),
        'subtitle': _('List of all AirERP aircrafts')
    }


class AircraftManagerUpdateView(SuccessMessageMixin, UpdateView):
    model = Aircraft
    form_class = AircraftManagerForm
    template_name = 'manager/apps/aircraft/aircraft.html'
    context_object_name = 'aircraft'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-aircrafts')
    extra_context = {
        'title': _('Aircraft'),
        'subtitle': _('Detail information about aircraft')
    }


class AircraftManagerDeleteView(SuccessMessageMixin, DeleteView):
    model = Aircraft
    template_name = 'manager/apps/aircraft/aircraft.html'
    context_object_name = 'aircraft'
    success_url = reverse_lazy('manager-aircrafts')
    success_message = _('Delete object is successful')


class AircraftManagerCreateView(SuccessMessageMixin, CreateView):
    model = Aircraft
    form_class = AircraftManagerForm
    template_name = 'manager/apps/aircraft/aircraft.html'
    success_url = reverse_lazy('manager-aircrafts')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create aircraft'),
        'subtitle': _('Detail information about aircraft')
    }