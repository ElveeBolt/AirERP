from django.urls import path
from .views import (
    TicketManagerListView,
    TicketManagerUpdateView,
    TicketManagerDeleteView,
    TicketServiceManagerCreateView,
    TicketServiceManagerListView,
    TicketServiceManagerDeleteView,
    TicketServiceManagerDetailView,
    TicketCheckinManagerUpdateView,
    TicketOnboardingManagerUpdateView
)

urlpatterns = [
    path('', TicketManagerListView.as_view(), name='manager-tickets'),
    path('<int:pk>', TicketManagerUpdateView.as_view(), name='manager-ticket'),
    path('<int:pk>/delete', TicketManagerDeleteView.as_view(), name='manager-ticket-delete'),
    path('<int:pk>/services', TicketServiceManagerListView.as_view(), name='manager-ticket-services'),
    path('<int:pk>/services/create', TicketServiceManagerCreateView.as_view(), name='manager-ticket-service-create'),
    path('<int:pk>/services/<int:service_id>', TicketServiceManagerDetailView.as_view(), name='manager-ticket-service'),
    path('<int:pk>/services/<int:service_id>/delete', TicketServiceManagerDeleteView.as_view(), name='manager-ticket-service-delete'),
    path('<int:pk>/checkin/', TicketCheckinManagerUpdateView.as_view(), name='manager-ticket-checkin'),
    path('<int:pk>/onboarding/', TicketOnboardingManagerUpdateView.as_view(), name='manager-ticket-onboarding'),
]