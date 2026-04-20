from rest_framework import serializers
from django.utils import timezone
from django.db import transaction
from apps.registrations.models import Registrations
from apps.events.models import Event


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registrations
        fields = [
            'id',
            'full_name',
            'email',
            'phone_number',
            'organization',
            'event',
            'status',
            'check_in_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'check_in_at',
            'created_at',
            'updated_at',
        ]


    def validate_status(self, value):
        instance = self.instance
        if instance is None:
            return value

        allowed_transitions = {
            Registrations.STATUS_REGISTERED: [
                Registrations.STATUS_CANCELLED,
                Registrations.STATUS_CHECKED_IN,
            ],
            Registrations.STATUS_CHECKED_IN: [],
            Registrations.STATUS_CANCELLED: [Registrations.STATUS_REGISTERED],
        }

        current = instance.status
        if value != current and value not in allowed_transitions.get(current, []):
            raise serializers.ValidationError(
                f"Cannot change status from '{current}' to '{value}'."
            )
        return value

    def validate(self, data):
        event    = data.get('event')
        email    = data.get('email')
        instance = self.instance

        if event and email:
            existing_registration = Registrations.objects.filter(
                event=event,
                email=email,
                status=Registrations.STATUS_REGISTERED,
            )
            if instance:
                existing_registration = existing_registration.exclude(pk=instance.pk)

            if existing_registration.exists():
                raise serializers.ValidationError({
                    "email": "You have already registered for this event."
                })

        if instance is None and event:
            if event.current_capacity >= event.capacity:
                raise serializers.ValidationError({
                    "event": "Event is already full."
                })

        return data

    def create(self, validated_data):
        with transaction.atomic():
            event = Event.objects.select_for_update().get(
                pk=validated_data['event'].pk
            )

            if event.current_capacity >= event.capacity:
                raise serializers.ValidationError({
                    "event": "Event is already full."
                })

            event.current_capacity += 1
            event.save(update_fields=['current_capacity'])

            validated_data['event'] = event
            return Registrations.objects.create(**validated_data)

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=instance.event_id)

            if new_status == Registrations.STATUS_CANCELLED \
                    and instance.status != Registrations.STATUS_CANCELLED:
                if event.current_capacity > 0:
                    event.current_capacity -= 1
                    event.save(update_fields=['current_capacity'])

            elif new_status == Registrations.STATUS_CHECKED_IN \
                    and instance.status != Registrations.STATUS_CHECKED_IN:
                validated_data['check_in_at'] = timezone.now()

            elif new_status == Registrations.STATUS_REGISTERED \
                    and instance.status == Registrations.STATUS_CANCELLED:
                if event.current_capacity >= event.capacity:
                    raise serializers.ValidationError({
                        "event": "Event is already full, cannot re-register."
                    })
                event.current_capacity += 1
                event.save(update_fields=['current_capacity'])

            return super().update(instance, validated_data)


class RegistrationCancelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Registrations
        fields = ['id', 'status', 'updated_at']
        read_only_fields = ['id', 'updated_at']