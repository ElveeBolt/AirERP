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
from .tasks import send_email_task
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
        send_email_task.delay(
            template='user/emails/successful_signup.html',
            subject=_('Welcome to AirERP'),
            user_email=user_email
        )
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
