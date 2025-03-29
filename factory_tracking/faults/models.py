import os
import uuid
from datetime import datetime
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.html import format_html

class FaultStatus(models.TextChoices):
    OPEN = "OPEN", "Open"
    CLOSED = "CLOSED", "Closed"

class FaultCase(models.Model):
    # Required relationships
    machine = models.ForeignKey(
        'machinery.Machine',
        on_delete=models.CASCADE,
        related_name='faults',
        help_text="Machine that has the fault"
    )

    reported_by = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        related_name='reported_faults',
        limit_choices_to={'role__in': ['TECH', 'MANAGER']},
        help_text="Technician or Manager who reported the fault"
    )

    # Fault details
    description = models.TextField(
        help_text="Detailed description of the fault"
    )

    status = models.CharField(
        max_length=10,
        choices=FaultStatus.choices,
        default=FaultStatus.OPEN,
        help_text="Current status of the fault case"
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


def fault_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    fault_id = instance.fault_case.id if instance.fault_case.id else uuid.uuid4()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    filename = f"fault_{fault_id}_{timestamp}.{ext}"
    return os.path.join("fault_images", "unsaved" if isinstance(fault_id, uuid.UUID) else "", filename)


class FaultImage(models.Model):
    fault_case = models.ForeignKey(
        FaultCase,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Fault case related to this image"
    )
    image = models.ImageField(
        upload_to=fault_image_upload_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="An image showing the fault"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Fault #{self.fault_case.id}"

    def preview(self):
        if self.image and hasattr(self.image, 'url'):
            return format_html('<img src="{}" width="150" style="object-fit: contain;" />', self.image.url)
        return "(No image)"

    preview.short_description = "Preview"


class FaultNote(models.Model):
    fault_case = models.ForeignKey(
        FaultCase,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text="The fault this note is related to"
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.PROTECT,
        help_text="User who added the note"
    )
    content = models.TextField(
        help_text="Content of the note"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.author} on Fault #{self.fault_case.id}"


def fault_note_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    note_id = instance.note.id if instance.note.id else uuid.uuid4()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"note_{note_id}_{timestamp}.{ext}"
    return os.path.join("fault_notes", filename)


class FaultNoteImage(models.Model):
    note = models.ForeignKey(
        FaultNote,
        on_delete=models.CASCADE,
        related_name='images',
        help_text="Note related to this image"
    )
    image = models.ImageField(
        upload_to=fault_note_image_upload_path,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])],
        help_text="Image associated with the note"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Note #{self.note.id}"

    def preview(self):
        if self.image and hasattr(self.image, 'url'):
            return format_html('<img src="{}" width="150" style="object-fit: contain;" />', self.image.url)
        return "(No image)"

    preview.short_description = "Preview"
