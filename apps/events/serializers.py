from rest_framework import serializers
from .models import Event
from django.utils import timezone
from datetime import timedelta

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        """validate that title is at least 3 characters long"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value
    
    def validate_capacity(self, value):
        """validate that capacity is a positive integer"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Capacity must be a positive integer.")
        return value
    
    def validate(self, data):
        """
        Validate:
        - Event start/end times must be at least 1 day from now
        - Registration times must be at least 1 day from now
        - Event end time > event start time
        - Registration end time > registration start time
        """

        event_start_time = data.get('event_start_time')
        event_end_time = data.get('event_end_time')
        registration_start_time = data.get('registration_start_time')
        registration_end_time = data.get('registration_end_time')

        now = timezone.now()
        min_time = now + timedelta(days=1)

        if event_start_time and event_start_time < min_time:
            raise serializers.ValidationError("Event start time must be at least 1 day from now.")
        
        if registration_start_time and registration_start_time < min_time:
            raise serializers.ValidationError("Registration start time must be at least 1 day from now.")

        if event_start_time and event_end_time and event_end_time <= event_start_time:
            raise serializers.ValidationError("Event end time must be after the start time.")
        
        if registration_start_time and registration_end_time and registration_end_time <= registration_start_time:
            raise serializers.ValidationError("Registration end time must be after the registration start time.")
        
        """Check if venue has been booked by other event at the same time"""
        venue = data.get('venue')
        if venue and event_start_time and event_end_time:
            overlapping_events = Event.objects.filter(
                venue=venue,
                event_start_time__lt=event_end_time,
                event_end_time__gt=event_start_time
            )
            if self.instance:
                overlapping_events = overlapping_events.exclude(id=self.instance.id)
            if overlapping_events.exists():
                raise serializers.ValidationError("The selected venue is already booked for another event during the specified time.")
        
        return data