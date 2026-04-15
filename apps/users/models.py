import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),
        ("SPEAKER", "Speaker"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="USER"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'

    def __str__(self):
        return self.username