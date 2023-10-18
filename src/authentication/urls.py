from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from authentication import views

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("register/", views.user_registration, name='register')
]
