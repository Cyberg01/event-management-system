import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Registrations(models.Model):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='attendees'
    )
    session = models.ForeignKey(
        'event_sessions.Session',
        on_delete=models.SET_NULL,
        related_name='registrations'
    )
    track = models.ForeignKey(
        'tracks.Track',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registrations'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('registered', 'Registered'),
            ('cancelled', 'Cancelled'),
            ('waitlisted', 'Waitlisted')
        ],
        default='registered'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('attendee', 'event')
        db_table = 'registrations'
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.attendee.username} - {self.event.title} - {self.session.title}"