from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.users.models import UserProfile


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def validate_username(self, value):
        """Check if username is already in use"""
        if UserProfile.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value
    
    def validate_email(self, value):
        """Check if email is already in use"""
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'ADMIN'),
        )
        
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    role = serializers.ChoiceField(required=False, choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        
    def validate_email(self, value):
        """Check if email is already used by another user"""
        if not self.instance:
            return value
        
        user = self.instance
        if UserProfile.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    
    def validate_username(self, value):
        """Check if username is already used by another user"""
        if not self.instance:
            return value
        
        user = self.instance
        if UserProfile.objects.filter(username=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("Username is already in use.")
        return value
    
    def validate_password(self, value):
        """Validate password if provided"""
        if value:
            validate_password(value)

        """Validate if password not same with current password"""
        if self.instance and self.instance.check_password(value):
            raise serializers.ValidationError("New password cannot be the same as the current password.")
        return value