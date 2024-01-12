from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _


def send_successful_signup_email(user_email: str):
    message = render_to_string(
        template_name='emails/successful_signup.html',
        context={
            'user_email': user_email,
        }
    )
    email = EmailMessage(subject=_('Welcome to AirERP'), body=message, to=[user_email])
    email.send()
