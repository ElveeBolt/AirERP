from django.urls import path, include


urlpatterns = [
    path('', include('apps.page.urls_manager')),
    path('tickets/', include('apps.ticket.urls_manager')),
    path('aircrafts/', include('apps.aircraft.urls_manager')),
    path('airports/', include('apps.airport.urls_manager')),
    path('services/', include('apps.service.urls_manager')),
    path('flights/', include('apps.flight.urls_manager')),
]
