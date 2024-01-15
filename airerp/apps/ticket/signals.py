from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ticket


@receiver(post_save, sender=Ticket)
def update_flight_seat_availability(sender, instance, **kwargs):
    instance.flight.update_seat_availability()