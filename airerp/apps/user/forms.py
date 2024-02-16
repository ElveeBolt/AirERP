from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        label=_('Username:'),
        help_text=_('Username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter username...'),
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        required=True,
        label=_('Password:'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Enter password...'),
            'class': 'form-control'
        })
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter username...'),
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        required=True,
        label=_('First name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter first name...'),
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        required=True,
        label=_('Last name'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Enter last name...'),
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        label=_('Email'),
        widget=forms.EmailInput(attrs={
            'placeholder': _('Enter email...'),
            'class': 'form-control',
            'type': 'email'
        })
    )
    password1 = forms.CharField(
        required=True,
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': _('Enter password'),
            'class': 'form-control'
        })
    )
    password2 = forms.CharField(
        required=True,
        label=_('Repeat password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': _('Repeat password...'),
            'class': 'form-control'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        required=True,
        label=_('Current password:'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Enter password...'),
                'class': 'form-control'
            }
        )
    )
    new_password1 = forms.CharField(
        required=True,
        label=_('New password:'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Enter password...'),
                'class': 'form-control'
            }
        )
    )
    new_password2 = forms.CharField(
        required=True,
        label=_('Repeat new password:'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Enter password...'),
                'class': 'form-control'
            }
        )
    )


class UserGroupAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Select user'),
        widget=forms.Select(
            attrs={
                'placeholder': _('Select user...'),
                'class': 'form-control'
            }
        )
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label=_('Select group'),
        widget=forms.Select(
            attrs={
                'placeholder': _('Select group...'),
                'class': 'form-control'
            }
        )
    )
