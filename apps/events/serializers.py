from rest_framework import serializers
from apps.venues.serializers import VenueSerializer
from .models import Event
from apps.venues.models import Venue
from django.utils import timezone
from datetime import timedelta

class EventSerializer(serializers.ModelSerializer):
    venue = serializers.PrimaryKeyRelatedField(
        queryset=Venue.objects.all(),
        many=False,
        required=False
    )

    venue = VenueSerializer(read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id', 'creator', 'created_at', 'updated_at', 'current_capacity']
    
    def validate_title(self, value):
        """Validate that title is at least 3 characters long"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value
    
    def validate_capacity(self, value):
        """Validate that capacity is a positive integer"""
        if value is not None and value <= 0:
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
        venue = data.get('venue')

        now = timezone.now()
        min_time = now + timedelta(days=1)

        if event_start_time and event_start_time < min_time:
            raise serializers.ValidationError({"event_start_time": "Event start time must be at least 1 day from now."})
        
        if registration_start_time and registration_start_time < min_time:
            raise serializers.ValidationError({"registration_start_time": "Registration start time must be at least 1 day from now."})

        if event_start_time and event_end_time and event_end_time <= event_start_time:
            raise serializers.ValidationError({"event_end_time": "Event end time must be after the start time."})
        
        if registration_start_time and registration_end_time and registration_end_time <= registration_start_time:
            raise serializers.ValidationError({"registration_end_time": "Registration end time must be after the registration start time."})
        
        if registration_start_time and event_start_time and registration_start_time > event_start_time:
            raise serializers.ValidationError({"registration_start_time": "Registration start time must be before the event start time."})
        
        if registration_end_time and event_start_time and registration_end_time > event_start_time:
            raise serializers.ValidationError({"registration_end_time": "Registration end time must be before the event start time."})
        
        # Check if venue is booked by other events at the same time
        if venue and event_start_time and event_end_time:
            overlapping_events = Event.objects.filter(
                venue=venue,
                event_start_time__lt=event_end_time,
                event_end_time__gt=event_start_time
            )
            if self.instance:
                overlapping_events = overlapping_events.exclude(id=self.instance.id)
            if overlapping_events.exists():
                raise serializers.ValidationError({
                    "venue": f"The venue '{venue.name}' is already booked for another event during the specified time."
                })
        
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['creator'] = request.user
        
        validated_data['current_capacity'] = validated_data.get('capacity', 0)
        
        event = Event.objects.create(**validated_data)
        return event
    
    def update(self, instance, validated_data):
        # Update semua field termasuk venue (langsung, bukan .set())
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance
    
    """Override to_representation to exclude null values from the response"""
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {key: value for key, value in ret.items() if value is not None}