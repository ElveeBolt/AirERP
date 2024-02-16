import base64
import io

from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_email_task(subject, template, user_email):
    message = render_to_string(
        template_name=template,
        context={
            'user_email': user_email,
        }
    )

    email = EmailMessage(subject, body=message, to=[user_email])
    email.content_subtype = 'html'
    email.send()
