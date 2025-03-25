from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRole(models.TextChoices):
    TECHNICIAN = "TECH", "Technician"
    REPAIR = "REPAIR", "Repair"
    MANAGER = "MANAGER", "Manager"
    VIEW_ONLY = "VIEW", "View-only"

class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.VIEW_ONLY
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
