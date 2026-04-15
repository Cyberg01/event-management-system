from rest_framework import serializers
from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
    
    def validate(self, data):
        event = data.get('event')
        session = data.get('session')
        attendee = data.get('user')
        
        if not event:
            raise serializers.ValidationError({"event": "Event is required"})
        
        if not attendee:
            raise serializers.ValidationError({"attendee": "Attendee is required"})
        
        if not session:
            raise serializers.ValidationError({"session": "Session is required"})
        
        current_count = Registration.objects.filter(session=session).count()
        if current_count >= session.capacity:
            raise serializers.ValidationError({
                "session": f"Session '{session.title}' is at full capacity"
            })
        
        if Registration.objects.filter(attendee=attendee, event=event).exists():
            raise serializers.ValidationError({
                "registration": "You are already registered to this event"
            })
        
        return data