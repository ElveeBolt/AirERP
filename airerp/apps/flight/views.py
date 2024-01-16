from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ExpressionWrapper, F, DurationField
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView

from .forms import FlightManagerForm, FlightServiceManagerForm
from .models import Flight, FlightService
from apps.airport.models import Airport
from apps.ticket.models import Ticket
from apps.ticket.forms import TicketForm, TicketServiceFormSet
from apps.ticket.utils import generate_pdf
from apps.user.tasks import send_email_task
from apps.user.mixins import SupervisorManagerMixin


# Create your views here.
class FlightListView(ListView):
    model = Flight
    template_name = 'user/apps/flight/flights.html'
    context_object_name = 'flights'
    extra_context = {
        'title': _('Search results'),
        'subtitle': _('Compare prices. Book the best tickets. Enjoy your journey.')
    }

    def get_search_filters(self):
        departure_from = Airport.objects.get(id=self.request.GET.get('departure_from'))
        arrival_to = Airport.objects.get(id=self.request.GET.get('arrival_to'))

        return {
            'departure_from': departure_from,
            'arrival_to': arrival_to,
            'departure_time': self.request.GET.get('departure_time')
        }

    def get_queryset(self):
        filters = self.get_search_filters()
        queryset = self.model.objects.filter(
            departure_from=filters.get('departure_from'),
            arrival_to=filters.get('arrival_to'),
            departure_time__gte=filters.get('departure_time')
        ).annotate(
            duration=ExpressionWrapper(
                F('arrival_time') - F('departure_time'),
                output_field=DurationField()
            )
        )
        return queryset


class FlightDetailView(DetailView, FormMixin):
    model = Flight
    form_class = TicketForm
    template_name = 'user/apps/flight/flight.html'
    context_object_name = 'flight'
    success_url = reverse_lazy('confirm')
    extra_context = {
        'title': _('Flight'),
        'subtitle': _('Detail information about flight')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        context['free_seats'] = self.object.get_free_seats()
        return context

    def get_formset(self):
        flight_services = FlightService.objects.filter(flight_id=self.kwargs.get('pk'))
        formset = TicketServiceFormSet(initial=[{'service': flight_service} for flight_service in flight_services])
        formset.extra = flight_services.count()
        return formset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['flight'] = Flight.objects.get(pk=self.kwargs.get('pk'))
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = TicketServiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            form_instance = form.save(commit=False)
            form_instance.flight = Flight.objects.get(pk=self.kwargs.get('pk'))
            form_instance.user = self.request.user
            form_instance.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.ticket = form_instance
                instance.save()

            request.session['ticket'] = form_instance.pk

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ConfirmView(TemplateView):
    template_name = 'user/apps/flight/confirm.html'
    extra_context = {
        'title': _('Confirm'),
        'subtitle': _('Detail information about your ticket')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_ticket()
        context['ticket'] = ticket
        context['ticket_total_price'] = ticket.calculate_total_price()
        return context

    def get_ticket(self):
        ticket_id = self.request.session.get('ticket')
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket


class ThanksView(TemplateView):
    template_name = 'user/apps/flight/thanks.html'
    extra_context = {
        'title': _('Thanks'),
        'subtitle': _('Detail information about your ticket')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = self.get_ticket()
        context['ticket'] = ticket

        buffer = generate_pdf(ticket_id=ticket.id)

        send_email_task.delay(
            template='user/emails/ticket.html',
            subject=_('Your ticket AirERP'),
            user_email=ticket.user.email,
            attach={
                'filename': 'ticket.pdf',
                'content': buffer,
                'mimetype': 'application/pdf'
            }
        )

        return context

    def get_ticket(self):
        ticket_id = self.request.session.get('ticket')
        ticket = Ticket.objects.get(id=ticket_id)
        return ticket


class FlightManagerListView(SupervisorManagerMixin, ListView):
    model = Flight
    template_name = 'manager/apps/flight/flights.html'
    context_object_name = 'flights'
    extra_context = {
        'title': _('Flights'),
        'subtitle': _('List of all AirERP flights')
    }


class FlightManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
    model = Flight
    form_class = FlightManagerForm
    template_name = 'manager/apps/flight/flight.html'
    context_object_name = 'flight'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-flights')
    extra_context = {
        'title': _('Flight'),
        'subtitle': _('Detail information about flight')
    }


class FlightManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = Flight
    success_url = reverse_lazy('manager-flights')
    success_message = _('Delete object is successful')


class FlightManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = Flight
    form_class = FlightManagerForm
    template_name = 'manager/apps/flight/flight.html'
    success_url = reverse_lazy('manager-flights')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create flight'),
        'subtitle': _('Detail information about flight')
    }


class FlightServiceManagerListView(SupervisorManagerMixin, ListView):
    model = FlightService
    template_name = 'manager/apps/flight/services.html'
    context_object_name = 'services'
    extra_context = {
        'title': _('Flight Services'),
        'subtitle': _('List of all AirERP flight services')
    }


class FlightServiceManagerUpdateView(SupervisorManagerMixin, SuccessMessageMixin, UpdateView):
    model = FlightService
    form_class = FlightServiceManagerForm
    template_name = 'manager/apps/flight/service.html'
    context_object_name = 'flight'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-flight-services')
    extra_context = {
        'title': _('Flight service'),
        'subtitle': _('Detail information about flight service')
    }


class FlightServiceManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = FlightService
    success_url = reverse_lazy('manager-flight-services')
    success_message = _('Delete object is successful')


class FlightServiceManagerCreateView(SupervisorManagerMixin, SuccessMessageMixin, CreateView):
    model = FlightService
    form_class = FlightServiceManagerForm
    template_name = 'manager/apps/flight/service.html'
    success_url = reverse_lazy('manager-flight-services')
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Create flight service'),
        'subtitle': _('Detail information about flight service')
    }