import uuid
from django.db import models
from django.conf import settings


class Speaker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255, blank=False, help_text="Speaker full name")
    email = models.EmailField(blank=True, null=True, help_text="Speaker contact email")
    bio = models.TextField(blank=True, null=True, help_text="Speaker biography")
    title = models.CharField(max_length=255, help_text="Professional title (e.g., Senior Engineer at Google)")
    company = models.CharField(max_length=255, blank=True, null=True)
    social_links = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text="Social media links: {photo, linkedin, twitter, website, github, etc}"
    )
    expertise = models.JSONField(
        blank=True,
        null=True,
        default=list,
        help_text="Array of expertise areas: ['Python', 'AI', 'Cloud']"
    )
    metadata = models.JSONField(
        blank=True,
        null=True,
        default=dict,
        help_text="Additional speaker information"
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='speakers',
        help_text="User who created this speaker"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'speakers'
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.title}"