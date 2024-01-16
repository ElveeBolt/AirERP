from django.urls import path

from .consumers import TicketStatusConsumer

websocket_urlpatterns = [
    path('ws/manager/tickets/', TicketStatusConsumer.as_asgi()),
]