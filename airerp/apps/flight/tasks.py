from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.ticket.utils import generate_pdf


@shared_task
def send_email_ticket_task(subject, template, user_email, ticket_id):
    message = render_to_string(
        template_name=template,
        context={
            'user_email': user_email,
        }
    )

    buffer = generate_pdf(ticket_id=ticket_id)

    email = EmailMessage(subject, body=message, to=[user_email])
    email.content_subtype = 'html'
    email.attach(filename='ticket.pdf', content=buffer.getvalue(), mimetype='application/pdf')
    email.send()
