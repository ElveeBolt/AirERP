from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, ListView, CreateView, DetailView
from django.utils.translation import gettext_lazy as _

from .forms import TicketManagerForm, TicketServiceManagerForm
from .models import Ticket, TicketService


# Create your views here.
class TicketManagerListView(ListView):
    model = Ticket
    template_name = 'manager/apps/ticket/tickets.html'
    context_object_name = 'tickets'
    extra_context = {
        'title': _('Tickets'),
        'subtitle': _('List of all AirERP tickets')
    }


class TicketManagerUpdateView(SuccessMessageMixin, UpdateView):
    model = Ticket
    form_class = TicketManagerForm
    template_name = 'manager/apps/ticket/ticket.html'
    context_object_name = 'ticket'
    success_message = _('Update object is successful')
    success_url = reverse_lazy('manager-tickets')
    extra_context = {
        'title': _('Ticket'),
        'subtitle': _('Detail information about ticket')
    }


class TicketManagerDeleteView(SuccessMessageMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('manager-tickets')
    success_message = _('Delete object is successful')


class TicketServiceManagerCreateView(SuccessMessageMixin, CreateView):
    model = TicketService
    form_class = TicketServiceManagerForm
    template_name = 'manager/apps/ticket/service.html'
    context_object_name = 'ticket'
    success_message = _('Create object is successful')
    extra_context = {
        'title': _('Ticket'),
        'subtitle': _('Detail information about ticket')
    }

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        kwargs['services'] = ticket.flight.flightservice_set.all()
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
            form_instance.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('manager-ticket', args=[self.kwargs.get('pk')])


class TicketServiceManagerListView(ListView):
    model = TicketService
    template_name = 'manager/apps/ticket/services.html'
    context_object_name = 'services'
    extra_context = {
        'title': _('Ticket services'),
        'subtitle': _('List of all AirERP ticket services')
    }

    def get_queryset(self):
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        queryset = TicketService.objects.filter(ticket=ticket)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(pk=self.kwargs.get('pk'))
        return context


class TicketServiceManagerDetailView(DetailView):
    model = TicketService
    template_name = 'manager/apps/ticket/service-detail.html'
    context_object_name = 'service'
    pk_url_kwarg = 'service_id'
    extra_context = {
        'title': _('Ticket service'),
        'subtitle': _('List of all AirERP ticket service')
    }


class TicketServiceManagerDeleteView(SuccessMessageMixin, DeleteView):
    model = TicketService
    success_url = reverse_lazy('manager-tickets')
    pk_url_kwarg = 'service_id'
    success_message = _('Delete object is successful')