from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
    
    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        return event
        
class VenueSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    name = serializers.CharField(required=True, max_length=255)
    description = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    link = serializers.URLField(required=False)

    def validate(self, value):
        venue_type = value.get('type', '').lower()

        if venue_type == 'online':
            if not value.get('link'):
                raise serializers.ValidationError("Link is required for online venues.")
        return value