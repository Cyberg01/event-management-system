import uuid

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

EVENT_STATUS = (
    ('upcoming', 'Upcoming'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)

EVENT_TYPE = (
    ('online', 'Online'),
    ('in-person', 'In-Person'),
    ('hybrid', 'Hybrid')
)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=False)
    status = models.CharField(
        max_length=50, 
        default='upcoming', 
        choices=EVENT_STATUS
        )
    event_type = models.CharField(
        max_length=50,
        choices=EVENT_TYPE,
        default='online'
    )
    capacity = models.PositiveIntegerField(null=False, default=10)
    event_start_time = models.DateTimeField()
    event_end_time = models.DateTimeField()
    registration_start_time = models.DateTimeField()
    registration_end_time = models.DateTimeField()
    creator_id = models.ForeignKey(
        'users.UserProfile', 
        related_name='created_events', 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    venue_id = models.ForeignKey(
        'venues.Venue', 
        related_name='created_events', 
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        )
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-event_start_time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def clean(self):
        if self.event_start_time < timezone.now():
            raise ValidationError('Event start time cannot be in the past.')
        if self.event_end_time <= self.event_start_time:
            raise ValidationError('Event end time must be after the start time.')
        if self.registration_start_time < timezone.now():
            raise ValidationError('Registration start time cannot be in the past.')
        if self.registration_end_time <= self.registration_start_time:
            raise ValidationError('Registration end time must be after the registration start time.')
            
    def __str__(self):
        return self.title