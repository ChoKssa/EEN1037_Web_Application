from django.urls import path

from . import views

urlpatterns = [
    path("faults/", views.faults, name="faults"),
]
