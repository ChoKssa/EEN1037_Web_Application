from django.urls import path

from . import views

urlpatterns = [
    path("faults/", views.faults, name="faults"),
    path("faults/<int:id>/", views.fault_detail, name="fault_detail"),
]
