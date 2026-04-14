from rest_framework import serializers
from apps.users.models import UserProfile
from django.contrib.auth.password_validation import validate_password

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserProfile.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer to update user profile (without password)"""
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def validate_email(self, value):
        """Check if email is unique (if changed)"""
        if not self.instance:  # ← CEK DULU
            return value
        
        user = self.instance
        if UserProfile.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_username(self, value):
        """Check if username is unique (if changed)"""
        if not self.instance:  # ← CEK DULU
            return value
        
        user = self.instance
        if UserProfile.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value