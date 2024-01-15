from django.urls import path, include


urlpatterns = [
    path('aircrafts/', include('apps.aircraft.urls_manager')),
]
