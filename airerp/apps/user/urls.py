from django.urls import path, include
from .views import (
    UserLoginView,
    UserSignUpView,
    UserLogoutView,
    UserView,
    UserChangePasswordView,
    UserTicketListView,
    UserTicketDetailView,
    UserTicketPDFView
)

urlpatterns = [
    path('', UserView.as_view(), name='user'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('social-login/', include('social_django.urls', namespace='social')),

    path('tickets/', UserTicketListView.as_view(), name='user-tickets'),
    path('tickets/<int:pk>', UserTicketDetailView.as_view(), name='user-ticket'),
    path('tickets/<int:pk>/pdf', UserTicketPDFView.as_view(), name='user-ticket-pdf')

]