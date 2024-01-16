from django.urls import path
from .views import (
    UserManagerListView,
    UserManagerUpdateView,
    UserManagerDeleteView
)

urlpatterns = [
    path('', UserManagerListView.as_view(), name='manager-users'),
    path('<int:pk>', UserManagerUpdateView.as_view(), name='manager-user'),
    path('<int:pk>/delete/', UserManagerDeleteView.as_view(), name='manager-user-delete'),
]