from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, ListView
from django.utils.translation import gettext_lazy as _

from .forms import TicketManagerForm
from .models import Ticket


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