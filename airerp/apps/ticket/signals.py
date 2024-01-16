import channels
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ticket


@receiver(post_save, sender=Ticket)
def update_flight_seat_availability(sender, instance, **kwargs):
    instance.flight.update_seat_availability()

    channel_layer = channels.layers.get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'ticket_status',
        {
            'type': 'send_ticket_status',
            'data': {
                "ticket_id": instance.id,
                "is_checkin": instance.is_checkin,
                "is_onboarding": instance.is_onboarding
            }
        }
    )
