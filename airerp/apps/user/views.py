from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView, DeleteView, FormView

from apps.ticket.models import Ticket
from apps.ticket.utils import generate_pdf

from .forms import LoginForm, SignUpForm, ChangePasswordForm, UserGroupAssignmentForm
from .mixins import SupervisorManagerMixin
from .tasks import send_email_task
from .models import User


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


class UserChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'user/apps/user/change_password.html'
    success_url = reverse_lazy('change-password')
    success_message = _('Change user password is success')
    form_class = ChangePasswordForm
    extra_context = {
        'title': _('Change password'),
        'subtitle': _('Password change page')
    }


class UserTicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'user/apps/user/tickets.html'
    context_object_name = 'tickets'
    extra_context = {
        'title': _('My tickets'),
        'subtitle': _('My ticket history')
    }

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class UserTicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'user/apps/user/ticket.html'
    context_object_name = 'ticket'
    extra_context = {
        'title': _('My ticket'),
        'subtitle': _('Detail information about ticket')
    }


class UserTicketPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('pk')

        buffer = generate_pdf(ticket_id=ticket_id)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="ticket_{ticket_id}.pdf"'
        return response


class UserManagerListView(SupervisorManagerMixin, ListView):
    model = User
    template_name = 'manager/apps/user/users.html'
    context_object_name = 'users'
    extra_context = {
        'title': _('Users'),
        'subtitle': _('List of all AirERP users')
    }

    def get_queryset(self):
        queryset = User.objects.filter()
        return queryset


class UserManagerUpdateView(SupervisorManagerMixin, FormView):
    template_name = 'manager/apps/user/user.html'
    form_class = UserGroupAssignmentForm
    success_url = reverse_lazy('manager-users')
    extra_context = {
        'title': _('User Assign'),
        'subtitle': _('Detail information about user assign')
    }

    def get_initial(self):
        initial = super().get_initial()
        user = User.objects.get(pk=self.kwargs.get('pk'))
        initial['user'] = user

        user_groups = user.groups.all()
        if user_groups:
            initial['group'] = user_groups[0]
        return initial

    def form_valid(self, form):
        user = form.cleaned_data['user']
        group = form.cleaned_data['group']
        user.groups.set([group])
        return super().form_valid(form)


class UserManagerDeleteView(SupervisorManagerMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('manager-users')
    success_message = _('Delete object is successful')