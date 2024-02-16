from django.urls import path
from .views import (
    FlightManagerListView,
    FlightManagerUpdateView,
    FlightManagerDeleteView,
    FlightManagerCreateView,
    FlightServiceManagerListView,
    FlightServiceManagerUpdateView,
    FlightServiceManagerDeleteView,
    FlightServiceManagerCreateView,
)

urlpatterns = [
    path('', FlightManagerListView.as_view(), name='manager-flights'),
    path('create/', FlightManagerCreateView.as_view(), name='manager-flight-create'),
    path('<int:pk>', FlightManagerUpdateView.as_view(), name='manager-flight'),
    path('<int:pk>/delete/', FlightManagerDeleteView.as_view(), name='manager-flight-delete'),

    path('services/', FlightServiceManagerListView.as_view(), name='manager-flight-services'),
    path('services/create/', FlightServiceManagerCreateView.as_view(), name='manager-flight-service-create'),
    path('services/<int:pk>', FlightServiceManagerUpdateView.as_view(), name='manager-flight-service'),
    path('services/<int:pk>/delete/', FlightServiceManagerDeleteView.as_view(), name='manager-flight-service-delete'),
]
