from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Flight


@receiver(post_save, sender=Flight)
def update_flight_seat_availability(sender, instance, **kwargs):
    instance.update_free_seats()
    instance.save_aircraft_current_airport()
