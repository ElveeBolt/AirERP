import io

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import A4
from django.utils.translation import gettext_lazy as _

from .models import Ticket


def generate_pdf(ticket_id: int):
    ticket = Ticket.objects.get(id=ticket_id)
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    title_text = f'Ticket code: {ticket.code}'
    title = Paragraph(title_text, styles["Heading1"])
    story.append(title)
    story.append(Spacer(1, 12))

    flight_info_text = f"""
    {ticket.flight.departure_from} --> {ticket.flight.arrival_to}<br/>
    {ticket.flight.departure_time} --> {ticket.flight.arrival_time}
    """
    flight_info = Paragraph(flight_info_text, styles["Normal"])
    story.append(flight_info)
    story.append(Spacer(1, 12))

    passanger_info_text = f"""
    First name: {ticket.first_name}<br/>
    Last name: {ticket.last_name}<br/>
    Date birth: {ticket.date_birth}<br/>
    Gender: {ticket.gender}<br/><br/>
    Document type: {ticket.document_type}<br/>
    Document serial: {ticket.document_serial}<br/>
    Document date expiry: {ticket.document_date_expiry}<br/>
    """
    passanger_info = Paragraph(passanger_info_text, styles["Normal"])
    story.append(passanger_info)
    story.append(Spacer(1, 12))

    buffer.seek(0)
    doc.build(story)
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
