import uuid
from django.db import models


class Registrations(models.Model):

    STATUS_REGISTERED = 'registered'
    STATUS_CHECKED_IN = 'checked_in'
    STATUS_CANCELLED  = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_REGISTERED, 'Registered'),
        (STATUS_CHECKED_IN, 'Checked In'),
        (STATUS_CANCELLED,  'Cancelled'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='attendees'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_REGISTERED,
    )
    check_in_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registrations'
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"