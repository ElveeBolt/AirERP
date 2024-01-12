from django.urls import path
from .views import (
    ManagerTicketListView,
    ManagerTicketDetailView,
    ManagerTicketUpdateOnboardingView,
    ManagerTicketUpdateCheckinView,
    ManagerView
)

urlpatterns = [
    path('', ManagerView.as_view(), name='manager'),
    path('tickets/', ManagerTicketListView.as_view(), name='manager-tickets'),
    path('tickets/<int:pk>', ManagerTicketDetailView.as_view(), name='manager-ticket'),
    path('tickets/<int:pk>/onboarding', ManagerTicketUpdateOnboardingView.as_view(), name='manager-ticket-onboarding'),
    path('tickets/<int:pk>/checkin', ManagerTicketUpdateCheckinView.as_view(), name='manager-ticket-checkin'),
]


