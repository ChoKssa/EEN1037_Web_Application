from django.urls import path

from . import views

urlpatterns = [
    path("machines", views.machines, name="machines"),
]
