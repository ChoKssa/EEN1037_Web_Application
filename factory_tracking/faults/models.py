from django.db import models
from django.core.validators import FileExtensionValidator

class FaultStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"

class FaultCase(models.Model):
    # Required relationships
    machine = models.ForeignKey(
        'Machine',
        on_delete=models.CASCADE,
        related_name='faults',
        help_text="Machine that has the fault"
    )
    
    reported_by = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='reported_faults',
        limit_choices_to={'role': 'TECH'},
        help_text="Technician who reported the fault"
    )

    # Fault details
    description = models.TextField(
        help_text="Detailed description of the fault"
    )
    
    images = models.FileField(
        upload_to='fault_images/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Images showing the fault (optional)"
    )
    
    status = models.CharField(
        max_length=10,
        choices=FaultStatus.choices,
        default=FaultStatus.OPEN,
        help_text="Current status of the fault case"
    )
    
    notes = models.JSONField(
        default=list,
        help_text="List of notes added by Technicians and Repairers"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the fault was resolved"
    )

    def __str__(self):
        return f"Fault #{self.id} - {self.machine.name} ({self.status})"

    class Meta:
        ordering = ['-created_at']  # Newest faults first 