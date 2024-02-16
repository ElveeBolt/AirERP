from django.urls import path
from .views import AircraftListView, AircraftDetailView

urlpatterns = [
    path('', AircraftListView.as_view(), name='aircrafts'),
    path('<int:pk>', AircraftDetailView.as_view(), name='aircraft'),
]
