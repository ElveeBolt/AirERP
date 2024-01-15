from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, ListView
from django.utils.translation import gettext_lazy as _

from .forms import ServiceManagerForm, BaggageManagerForm
from .models import Service, Baggage


# Create your views here.
class ServiceManagerListView(ListView):
    model = Service
    template_name = 'manager/apps/service/services.html'
    context_object_name = 'services'
    extra_context = {
        'title': _('Services'),
        'subtitle': _('List of all AirERP services')
    }


class ServiceManagerUpdateView(SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceManagerForm
    template_name = 'manager/apps/service/service.html'
    context_object_name = 'service'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-services')
    extra_context = {
        'title': _('Service'),
        'subtitle': _('Detail information about service')
    }


class ServiceManagerDeleteView(SuccessMessageMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('manager-services')
    success_message = _('Delete object is successful')


class ServiceManagerCreateView(SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceManagerForm
    template_name = 'manager/apps/service/service.html'
    success_url = reverse_lazy('manager-services')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create service'),
        'subtitle': _('Detail information about service')
    }


class BaggageManagerListView(ListView):
    model = Baggage
    template_name = 'manager/apps/service/baggages.html'
    context_object_name = 'baggages'
    extra_context = {
        'title': _('Baggages'),
        'subtitle': _('List of all AirERP baggages')
    }


class BaggageManagerUpdateView(SuccessMessageMixin, UpdateView):
    model = Baggage
    form_class = BaggageManagerForm
    template_name = 'manager/apps/service/baggage.html'
    context_object_name = 'baggage'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-service-baggages')
    extra_context = {
        'title': _('Baggage'),
        'subtitle': _('Detail information about baggage')
    }


class BaggageManagerDeleteView(SuccessMessageMixin, DeleteView):
    model = Baggage
    success_url = reverse_lazy('manager-service-baggages')
    success_message = _('Delete object is successful')


class BaggageManagerCreateView(SuccessMessageMixin, CreateView):
    model = Baggage
    form_class = BaggageManagerForm
    template_name = 'manager/apps/service/baggage.html'
    success_url = reverse_lazy('manager-service-baggages')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create baggage'),
        'subtitle': _('Detail information about baggage')
    }