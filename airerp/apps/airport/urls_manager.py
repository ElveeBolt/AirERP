from django.urls import path
from .views import (
    AirportManagerListView,
    AirportManagerUpdateView,
    AirportManagerDeleteView,
    AirportManagerCreateView,
    CityManagerListView,
    CityManagerUpdateView,
    CityManagerDeleteView,
    CityManagerCreateView
)

urlpatterns = [
    path('', AirportManagerListView.as_view(), name='manager-airports'),
    path('create/', AirportManagerCreateView.as_view(), name='manager-airport-create'),
    path('<int:pk>', AirportManagerUpdateView.as_view(), name='manager-airport'),
    path('<int:pk>/delete/', AirportManagerDeleteView.as_view(), name='manager-airport-delete'),

    path('cities/', CityManagerListView.as_view(), name='manager-airport-cities'),
    path('cities/create/', CityManagerCreateView.as_view(), name='manager-airport-city-create'),
    path('cities/<int:pk>', CityManagerUpdateView.as_view(), name='manager-airport-city'),
    path('cities/<int:pk>/delete/', CityManagerDeleteView.as_view(), name='manager-airport-city-delete'),
]
