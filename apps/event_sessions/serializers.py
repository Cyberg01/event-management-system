from rest_framework import serializers
from apps.tracks.models import Track
from .models import Sessions
from apps.events.models import Event

class SessionsSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
        error_messages={
            'required': 'Event is required.',
            'does_not_exist': 'Event with id {pk_value} does not exist.',
            'null': 'Event is required.',
            'invalid': 'Invalid event ID format.'
        }
    )

    tracks = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(),
        required=True,
        allow_null=False,
        error_messages={
            'does_not_exist': 'Track with id {pk_value} does not exist.',
            'invalid': 'Invalid track ID format.'
        }
    )
    

    event_title = serializers.CharField(source='event.title', read_only=True)
    event_start = serializers.DateTimeField(source='event.event_start_time', read_only=True)
    event_end = serializers.DateTimeField(source='event.event_end_time', read_only=True)
    track_name = serializers.CharField(source='tracks.name', read_only=True)
    
    class Meta:
        model = Sessions
        fields = [
            'id', 'title', 'description',
            'start_time', 'end_time', 'creator', 'event', 'tracks',
            'created_at', 'updated_at',
            'event_title', 'event_start', 'event_end', 'track_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'creator']\

    
    def validate(self, data):
        """Validate session data including time conflicts and boundaries"""
        start_time = data.get('start_time', self.instance.start_time if self.instance else None)
        end_time = data.get('end_time', self.instance.end_time if self.instance else None)
        event = data.get('event', self.instance.event if self.instance else None)
        tracks = data.get('tracks', self.instance.tracks if self.instance else None)

        
        """1. Validate start_time < end_time"""
        if start_time and end_time:
            if start_time >= end_time:
                raise serializers.ValidationError({
                    "start_time": "Start time must be before end time."
                })
        
        """2. Validate session times are within event boundaries"""
        if event and start_time and end_time:
            if start_time < event.event_start_time:
                raise serializers.ValidationError({
                    "start_time": f"Session start time must be after event start time ({event.event_start_time})."
                })
            if end_time > event.event_end_time:
                raise serializers.ValidationError({
                    "end_time": f"Session end time must be before event end time ({event.event_end_time})."
                })
            
        """3. Validate that all tracks belong to the selected event"""   
        if tracks and event:    
            if tracks.event != event:
                raise serializers.ValidationError({
                    "tracks": f"Track '{tracks.name}' does not belong to the selected event."
                })
                
        """4. Validate time conflicts with existing sessions in the same event and tracks"""
        if event and start_time and end_time and tracks:
            conflicting = Sessions.objects.filter(
            tracks=tracks,
            event=event,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(pk=self.instance.pk if self.instance else None)
            
            if conflicting.exists():
                raise serializers.ValidationError({
                    "time": "Session time conflicts with existing sessions in the same event and tracks."
                })
            
        """5. Validate session isn't duplicate in the same tracks and event"""
        if event and tracks:
            duplicate_sessions = Sessions.objects.filter(
                event=event,
                tracks=tracks,
                title=data.get('title')
            ).exclude(id=self.instance.id if self.instance else None)
        
        if duplicate_sessions.exists():
            raise serializers.ValidationError({
                "title": f"Session with title '{data.get('title')}' already exists in track '{tracks.name}'."
            })
        
        return data