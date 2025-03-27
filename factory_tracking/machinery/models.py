from django.db import models
from factory_tracking.users.models import User

class MachineStatus(models.TextChoices):
    OK = "OK", "OK"
    WARNING = "WARNING", "Warning"
    FAULT = "FAULT", "Fault"

class Machine(models.Model):
    # Required fields
    name = models.CharField(
        max_length=255,
        help_text="Name of the machine"
    )
    
    status = models.CharField(
        max_length=10,
        choices=MachineStatus.choices,
        default=MachineStatus.OK,
        help_text="Current status of the machine"
    )
    
    # Collections field - using ArrayField for multiple strings
    collections = models.JSONField(
        default=list,
        help_text="List of user-defined collection tags"
    )
    
    # Many-to-Many relationship with Users
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_machines',
        limit_choices_to={'role__in': ['TECH', 'REPAIR']},
        help_text="Technicians and Repairers assigned to this machine"
    )
    
    # Warning messages
    warnings = models.JSONField(
        default=list,
        help_text="List of active warning messages"
    )
    
    # Timestamps for record-keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    class Meta:
        ordering = ['name'] 