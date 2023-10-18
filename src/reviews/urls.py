from django.urls import path

from reviews import views

urlpatterns = [
    path("home/", views.home, name='home'),
]
