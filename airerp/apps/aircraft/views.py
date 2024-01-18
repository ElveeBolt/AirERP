from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from apps.user.mixins import SupervisorManagerMixin

from .models import AircraftModel, Aircraft
from .forms import AircraftManagerForm, AircraftModelManagerForm
from .filters import AircraftFilter


# Create your views here.
class AircraftListView(FilterView):
    model = AircraftModel
    template_name = 'user/apps/aircraft/aircrafts.html'
    context_object_name = 'aircrafts'
    paginate_by = settings.PAGINATION_COUNT
    filterset_class = AircraftFilter
    extra_context = {
        'title': _('Aircrafts'),
        'subtitle': _('List of all AirERP aircrafts')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['querystring'] = self.get_querystring()
        return context

    def get_querystring(self):
        if self.request.GET:
            querystring = self.request.GET.copy()
            if self.request.GET.get('page'):
                del querystring['page']
            return querystring.urlencode()


class AircraftDetailView(DetailView):
    model = AircraftModel
    template_name = 'user/apps/aircraft/aircraft.html'
    context_object_name = 'aircraft'
    extra_context = {
        'title': _('Aircraft'),
        'subtitle': _('Detail information about aircraft')
    }


# Views for managers.
class AircraftManagerListView(SupervisorManagerMixin, ListView):
    model = Aircraft
    template_name = 'manager/apps/aircraft/aircrafts.html'
    context_object_name = 'aircrafts'
    extra_context = {
        'title': _('Aircrafts'),
        'subtitle': _('List of all AirERP aircrafts')
    }


class AircraftManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
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


class AircraftManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = Aircraft
    template_name = 'manager/apps/aircraft/aircraft.html'
    context_object_name = 'aircraft'
    success_url = reverse_lazy('manager-aircrafts')
    success_message = _('Delete object is successful')


class AircraftManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = Aircraft
    form_class = AircraftManagerForm
    template_name = 'manager/apps/aircraft/aircraft.html'
    success_url = reverse_lazy('manager-aircrafts')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create aircraft'),
        'subtitle': _('Detail information about aircraft')
    }


class AircraftModelManagerListView(SupervisorManagerMixin, ListView):
    model = AircraftModel
    template_name = 'manager/apps/aircraft/aircraft-models.html'
    context_object_name = 'aircrafts'
    extra_context = {
        'title': _('Aircraft models'),
        'subtitle': _('List of all AirERP aircraft models')
    }


class AircraftModelManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
    model = AircraftModel
    form_class = AircraftModelManagerForm
    template_name = 'manager/apps/aircraft/aircraft-model.html'
    context_object_name = 'aircraft'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-aircraft-models')
    extra_context = {
        'title': _('Aircraft model'),
        'subtitle': _('Detail information about aircraft model')
    }


class AircraftModelManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = AircraftModel
    template_name = 'manager/apps/aircraft/aircraft-model.html'
    context_object_name = 'aircraft'
    success_url = reverse_lazy('manager-aircraft-models')
    success_message = _('Delete object is successful')


class AircraftModelManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = AircraftModel
    form_class = AircraftModelManagerForm
    template_name = 'manager/apps/aircraft/aircraft-model.html'
    success_url = reverse_lazy('manager-aircraft-models')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create aircraft model'),
        'subtitle': _('Detail information about aircraft model')
    }