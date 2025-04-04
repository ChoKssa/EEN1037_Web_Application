from django.urls import path

from . import views

urlpatterns = [
    path("faults/", views.fault_list, name="faults"),
    path("faults/create/", views.create_fault, name="create_fault"),
    path("faults/<int:fault_id>/", views.fault_detail, name="fault_detail"),
    path("faults/<int:fault_id>/add-note/", views.add_fault_note, name="add_fault_note"),
    path("faults/<int:fault_id>/close/", views.close_fault, name="close_fault"),
]
