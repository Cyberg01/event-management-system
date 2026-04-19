import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Sessions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    event = models.ForeignKey(
        'events.Event', 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    tracks = models.ForeignKey(
        'tracks.Track',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sessions'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sessions'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} - {self.event.title}"
    
    def clean(self):
        """Validate session times and constraints"""
        errors = {}
        
        # Validate start_time < end_time
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                errors['start_time'] = 'Start time must be before end time.'
        
        """Validate session is within event time boundaries"""
        if self.event and self.start_time and self.end_time:
            if self.start_time < self.event.event_start_time:
                errors['start_time'] = 'Session start time must be after event start time.'
            if self.end_time > self.event.event_end_time:
                errors['end_time'] = 'Session end time must be before event end time.'
        
        if errors:
            raise ValidationError(errors)