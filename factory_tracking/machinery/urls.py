from django.urls import path

from . import views

urlpatterns = [
    path("machines", views.machines, name="machines"),
    path("machines/create/", views.create_machine, name="create_machine"),
    path("machines/<int:machine_id>/", views.machine_detail, name="machine_detail"),
    path("machines/<int:machine_id>/update/", views.edit_machine, name="update_machine"),
    path("machines/<int:machine_id>/delete/", views.delete_machine, name="delete_machine"),
    path("machines/<int:machine_id>/add-warning/", views.add_warning, name="add_warning"),
    path("machines/<int:machine_id>/delete-warning/", views.delete_warning, name="delete_warning"),
]
