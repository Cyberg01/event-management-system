import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color code, e.g. #FF5733")
    metadata = models.JSONField(blank=True, null=True, help_text="Additional track information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tracks'
        verbose_name = 'Track'
        verbose_name_plural = 'Tracks'
        ordering = ['name']
        unique_together = ('event', 'name')
    
    def __str__(self):
        return f"{self.name} - {self.event.title}"
    
    def clean(self):
        """Validate color code if provided"""
        if self.color:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', self.color):
                raise ValidationError({
                    'color': 'Color must be a valid hex code (e.g., #FF5733)'
                })