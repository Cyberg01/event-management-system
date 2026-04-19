from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    name = serializers.UniqueTogetherValidator(
        queryset=Track.objects.all(), 
        fields=['event', 'name'], 
        message="Track with this name already exists in this Event."
    )

    def validate_event(self, value):
        if not value:
            raise serializers.ValidationError("Event is required to create a track.")
        return value
    
    def validate_color(self, value):
        """Validate hex color format"""
        if value:
            import re
            if not re.match(r'^#[0-9A-Fa-f]{6}$', value):
                raise serializers.ValidationError(
                    'Color must be a valid hex code (e.g., #FF5733)'
                )
        return value

    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['id', 'creator','created_at', 'updated_at']