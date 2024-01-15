from django.urls import path, include


urlpatterns = [
    path('', include('apps.page.urls_manager')),
    path('aircrafts/', include('apps.aircraft.urls_manager')),
    path('airports/', include('apps.airport.urls_manager')),
]
