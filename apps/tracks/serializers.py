from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        event = data.get('event')
        name = data.get('name')
        
        if not event:
            raise serializers.ValidationError({"event": "Event is required"})
        
        if not name:
            raise serializers.ValidationError({"name": "Track name is required"})
        
        if self.instance is None:
            if Track.objects.filter(event=event, name=name).exists():
                raise serializers.ValidationError({
                    "name": f"Track '{name}' already exists for this event"
                })
        else:
            existing = Track.objects.filter(event=event, name=name).exclude(id=self.instance.id)
            if existing.exists():
                raise serializers.ValidationError({
                    "name": f"Track '{name}' already exists for this event"
                })
        return data