from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

EVENT_STATUS = (
    ('upcoming', 'Upcoming'),
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled')
)

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=False)
    status = models.CharField(
        max_length=50, 
        default='upcoming', 
        choices=EVENT_STATUS
        )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    venue = models.JSONField()
    organizer = models.CharField(max_length=255)
    creatorId = models.ForeignKey(
        'users.UserProfile', 
        on_delete=models.CASCADE, 
        related_name='created_events'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def clean(self):
        if self.date < timezone.now().date():
            raise ValidationError('Event date cannot be in the past.')
            
    def __str__(self):
        return self.title