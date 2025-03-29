import re
from django.db import models
from users.models import User
from django.core.exceptions import ValidationError

def validate_collection_name(value):
    if not re.match(r'^[A-Za-z0-9\-]+$', value):
        raise ValidationError("Collection name must match [A-Za-z0-9\\-]")

class Collection(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[validate_collection_name],
        help_text="Collection name (e.g. Main-Campus, Floor-2)"
    )

    def __str__(self):
        return self.name


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

    collections = models.ManyToManyField(
        Collection,
        related_name='machines',
        help_text="User-defined tags like location or type"
    )

    # Many-to-Many relationship with Users
    assigned_users = models.ManyToManyField(
        User,
        related_name='assigned_machines',
        limit_choices_to={'role__in': ['TECH', 'REPAIR', 'MANAGER']},
        help_text="Technicians and Repairers assigned to this machine"
    )

    # Timestamps for record-keeping
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    class Meta:
        ordering = ['name']


class Warning(models.Model):
    machine = models.ForeignKey(
        'Machine',
        related_name='warnings',
        on_delete=models.CASCADE,
        help_text="Machine associated with this warning"
    )
    message = models.CharField(
        max_length=255,
        help_text="Free-form warning message"
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='added_warnings',
        help_text="User who added the warning"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('machine', 'message')
        ordering = ['-created_at']

    def __str__(self):
        return f"Warning on {self.machine.name}: {self.message}"
