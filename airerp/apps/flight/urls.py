from django.urls import path
from .views import FlightListView, FlightDetailView, ConfirmView, ThanksView

urlpatterns = [
    path('', FlightListView.as_view(), name='flights'),
    path('<int:pk>', FlightDetailView.as_view(), name='flight'),
    path('confirm/', ConfirmView.as_view(), name='confirm'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
]

