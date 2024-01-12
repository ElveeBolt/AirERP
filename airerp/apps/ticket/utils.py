import io

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.utils.translation import gettext_lazy as _

from .models import Ticket


def generate_pdf(ticket_id: int):
    ticket = Ticket.objects.get(id=ticket_id)
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.drawString(100, 750, f"Ticket code: {ticket.code}")
    pdf.drawString(100, 735, f"Passenger Name: {ticket.first_name} {ticket.last_name}")

    buffer.seek(0)
    pdf.save()
    return buffer


def send_ticket_email(user_email: str, ticket_id: int):
    buffer = generate_pdf(ticket_id=ticket_id)

    message = render_to_string(
        template_name='user/emails/ticket.html',
        context={
            'user_email': user_email,
        }
    )
    email = EmailMessage(subject=_('Your ticket AirERP'), body=message, to=[user_email])
    email.attach('ticket.pdf', buffer.getvalue(), 'application/pdf')
    email.send()
