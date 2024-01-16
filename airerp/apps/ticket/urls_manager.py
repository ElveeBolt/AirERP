from django.urls import path
from .views import (
    TicketManagerListView,
    TicketManagerUpdateView,
    TicketManagerDeleteView
)

urlpatterns = [
    path('', TicketManagerListView.as_view(), name='manager-tickets'),
    path('<int:pk>', TicketManagerUpdateView.as_view(), name='manager-ticket'),
    path('<int:pk>/delete', TicketManagerDeleteView.as_view(), name='manager-ticket-delete'),
]