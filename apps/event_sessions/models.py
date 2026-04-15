import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Sessions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        'events.Event', 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField(default=10)
    current_capacity = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speakers = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sessions'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} - {self.event.title}"