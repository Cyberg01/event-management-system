from rest_framework import serializers
from .models import Registrations

class RegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrations
        fields = '__all__'
    
    def validate(self, data):
        event = data.get('event')
        session = data.get('session')
        attendee = data.get('attendee')
        
        if not event:
            raise serializers.ValidationError({"event": "Event is required"})
        
        if not attendee:
            raise serializers.ValidationError({"attendee": "Attendee is required"})
        
        if not session:
            raise serializers.ValidationError({"session": "Session is required"})
        
        current_count = Registrations.objects.filter(session=session).count()
        if current_count >= session.capacity:
            raise serializers.ValidationError({
                "session": f"Session '{session.title}' is at full capacity"
            })
        
        if Registrations.objects.filter(attendee=attendee, event=event).exists():
            raise serializers.ValidationError({
                "registration": "You are already registered to this event"
            })
        
        return data