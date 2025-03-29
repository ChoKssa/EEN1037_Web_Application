from django.urls import path

from . import views

urlpatterns = [
    path("machines", views.machines, name="machines"),
    path("machines/<int:id>/", views.machine_detail, name="machine_detail"),
]
