from rest_framework import serializers
from .models import Sessions

class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'
    
    def create(self, validated_data):
        sessions = Sessions.objects.create(**validated_data)
        return sessions

    def get_speakers_data(self, obj):
        if obj.speakers:
            return obj.speakers
        return []
    
    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        
        event = data.get('event')
        if event and (data['start_time'] < event.event_start_time or data['end_time'] > event.event_end_time):
            raise serializers.ValidationError("Sessions times must be within the event duration.")
        
        conflicting = Sessions.objects.filter(
            event=data.get('event'),
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        ).exclude(pk=self.instance.pk if self.instance else None)
        
        if conflicting.exists():
            raise serializers.ValidationError("Sessions times conflict with another sessions in the same event.")
        return data