from django.urls import path
from . import views


# [TODO] Add API views for machines, warnings, and faults
urlpatterns = [
    # Machines
    # path("machines/", views.MachineCreateAPIView.as_view(), name="api-machine-create"),

    # Warnings
    # path("warnings/", views.WarningCreateAPIView.as_view(), name="api-warning-create"),

    # Faults
    # path("faults/", views.FaultCreateAPIView.as_view(), name="api-fault-create"),
    # path("faults/open/", views.OpenFaultListAPIView.as_view(), name="api-faults-open"),
    # path("faults/<int:pk>/", views.FaultDetailAPIView.as_view(), name="api-fault-detail"),
    # path("faults/<int:pk>/notes/", views.FaultNoteCreateAPIView.as_view(), name="api-faultnote-create"),
]
