from django.urls import path
from .views import AircraftManagerListView, AircraftManagerUpdateView, AircraftManagerDeleteView, AircraftManagerCreateView

urlpatterns = [
    path('', AircraftManagerListView.as_view(), name='manager-aircrafts'),
    path('create/', AircraftManagerCreateView.as_view(), name='manager-aircraft-create'),
    path('<int:pk>', AircraftManagerUpdateView.as_view(), name='manager-aircraft'),
    path('<int:pk>/delete/', AircraftManagerDeleteView.as_view(), name='manager-aircraft-delete'),
]
