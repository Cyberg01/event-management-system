from rest_framework import serializers
from .models import Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    """Basic speaker serializer for CRUD operations"""
    
    session_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Speaker
        fields = [
            'id', 'full_name', 'email', 'bio', 'title', 'company',
            'social_links', 'expertise', 'metadata', 'creator',
            'created_at', 'updated_at', 'session_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'creator']
    
    def get_session_count(self, obj):
        """Return number of sessions this speaker is assigned to"""
        return obj.sessions.count()
    
    def validate_email(self, value):
        """Validate email is unique if provided"""
        if value:
            exists = Speaker.objects.filter(email=value)
            if self.instance:
                exists = exists.exclude(pk=self.instance.pk)
            
            if exists.exists():
                raise serializers.ValidationError("A speaker with this email already exists.")
        
        return value