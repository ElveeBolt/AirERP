from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView

from apps.ticket.models import Ticket
from apps.ticket.utils import generate_pdf

from .forms import LoginForm, SignUpForm, ChangePasswordForm
from .utils import send_successful_signup_email
from .mixins import GateManagerMixin, CheckinManagerMixin, StaffMixin
from .manager_forms import OnboardingForm, CheckinForm
from ..flight.models import FlightService, Flight
from ..ticket.forms import TicketServiceFormSet


# Create your views here.
class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'user/apps/user/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title': _('Sign in'),
        'subtitle': _('To start using AirERP features, please login')
    }


class UserSignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'user/apps/user/signup.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')
    extra_context = {
        'title': _('Sign up'),
        'subtitle': _('To start using AirERP features, please signup')
    }

    def form_valid(self, form):
        response = super().form_valid(form)
        user_email = form.cleaned_data.get('email')
        send_successful_signup_email(user_email=user_email)
        return response


class UserLogoutView(LoginRequiredMixin, LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user/apps/user/user.html'
    extra_context = {
        'title': _('User'),
        'subtitle': _('Detailed information about user')
    }


class UserChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'user/apps/user/change_password.html'
    success_url = reverse_lazy('change-password')
    success_message = _('Change user password is success')
    form_class = ChangePasswordForm
    extra_context = {
        'title': _('Change password'),
        'subtitle': _('Password change page')
    }


class UserTicketListView(ListView):
    model = Ticket
    template_name = 'user/apps/user/tickets.html'
    context_object_name = 'tickets'
    extra_context = {
        'title': _('My tickets'),
        'subtitle': _('My ticket history')
    }

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserTicketDetailView(DetailView):
    model = Ticket
    template_name = 'user/apps/user/ticket.html'
    context_object_name = 'ticket'
    extra_context = {
        'title': _('My ticket'),
        'subtitle': _('Detail information about ticket')
    }


class UserTicketPDFView(View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('pk')

        buffer = generate_pdf(ticket_id=ticket_id)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="ticket_{ticket_id}.pdf"'
        return response


class ManagerView(StaffMixin, TemplateView):
    template_name = 'manager/index.html'
    extra_context = {
        'title': _('Index page'),
        'subtitle': _('Detail information about tickets')
    }


class ManagerTicketListView(GateManagerMixin, ListView):
    model = Ticket
    template_name = 'manager/apps/ticket/tickets.html'
    context_object_name = 'tickets'
    extra_context = {
        'title': _('Check tickets'),
        'subtitle': _('Detail information about tickets')
    }


class ManagerTicketDetailView(DetailView):
    model = Ticket
    template_name = 'manager/apps/ticket/ticket.html'
    context_object_name = 'ticket'
    extra_context = {
        'title': _('Ticket detail'),
        'subtitle': _('Detail information about ticket')
    }


class ManagerTicketUpdateOnboardingView(GateManagerMixin, UpdateView):
    model = Ticket
    form_class = OnboardingForm
    template_name = 'manager/apps/ticket/ticket-onboarding.html'
    context_object_name = 'ticket'
    success_url = reverse_lazy('manager-tickets')
    extra_context = {
        'title': _('Edit onboarding'),
        'subtitle': _('Edit ticket onboarding status')
    }


class ManagerTicketUpdateCheckinView(UpdateView):
    model = Ticket
    form_class = CheckinForm
    template_name = 'manager/apps/ticket/ticket-checkin.html'
    context_object_name = 'ticket'
    success_url = reverse_lazy('manager-tickets')
    extra_context = {
        'title': _('Edit checkin'),
        'subtitle': _('Edit ticket checkin status')
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def get_formset(self):
        object = self.get_object()
        flight_services = FlightService.objects.filter(flight_id=object.flight.pk)
        formset = TicketServiceFormSet(initial=[{'service': flight_service} for flight_service in flight_services])
        formset.extra = flight_services.count()
        return formset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['flight'] = self.get_object().flight
        return kwargs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = TicketServiceFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            form_instance = form.save(commit=False)
            form_instance.flight = self.get_object().flight
            form_instance.user = self.request.user
            form_instance.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.ticket = form_instance
                instance.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)