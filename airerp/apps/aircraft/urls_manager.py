from django.urls import path
from .views import (
    AircraftManagerListView,
    AircraftManagerUpdateView,
    AircraftManagerDeleteView,
    AircraftManagerCreateView,
    AircraftModelManagerListView,
    AircraftModelManagerUpdateView,
    AircraftModelManagerDeleteView,
    AircraftModelManagerCreateView
)

urlpatterns = [
    path('', AircraftManagerListView.as_view(), name='manager-aircrafts'),
    path('create/', AircraftManagerCreateView.as_view(), name='manager-aircraft-create'),
    path('<int:pk>', AircraftManagerUpdateView.as_view(), name='manager-aircraft'),
    path('<int:pk>/delete/', AircraftManagerDeleteView.as_view(), name='manager-aircraft-delete'),

    path('models', AircraftModelManagerListView.as_view(), name='manager-aircraft-models'),
    path('models/create/', AircraftModelManagerCreateView.as_view(), name='manager-aircraft-model-create'),
    path('models/<int:pk>', AircraftModelManagerUpdateView.as_view(), name='manager-aircraft-model'),
    path('models/<int:pk>/delete/', AircraftModelManagerDeleteView.as_view(), name='manager-aircraft-model-delete'),
]
