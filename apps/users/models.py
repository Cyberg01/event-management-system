from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("ATTENDEE", "Attendee"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="ATTENDEE"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username