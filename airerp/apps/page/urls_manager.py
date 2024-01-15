from django.urls import path
from .views import (
    IndexManagerView
)

urlpatterns = [
    path('', IndexManagerView.as_view(), name='manager'),
]
