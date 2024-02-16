from django.urls import path
from .views import (
    ServiceManagerListView,
    ServiceManagerUpdateView,
    ServiceManagerDeleteView,
    ServiceManagerCreateView,
    BaggageManagerListView,
    BaggageManagerUpdateView,
    BaggageManagerDeleteView,
    BaggageManagerCreateView
)

urlpatterns = [
    path('', ServiceManagerListView.as_view(), name='manager-services'),
    path('create/', ServiceManagerCreateView.as_view(), name='manager-service-create'),
    path('<int:pk>', ServiceManagerUpdateView.as_view(), name='manager-service'),
    path('<int:pk>/delete/', ServiceManagerDeleteView.as_view(), name='manager-service-delete'),

    path('baggages/', BaggageManagerListView.as_view(), name='manager-service-baggages'),
    path('baggages/create/', BaggageManagerCreateView.as_view(), name='manager-service-baggage-create'),
    path('baggages/<int:pk>', BaggageManagerUpdateView.as_view(), name='manager-service-baggage'),
    path('baggages/<int:pk>/delete/', BaggageManagerDeleteView.as_view(), name='manager-service-baggage-delete'),
]
