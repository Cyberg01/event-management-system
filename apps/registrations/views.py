from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from apps.events.models import Event
from .models import Registrations
from .serializers import RegistrationSerializer, RegistrationCancelSerializer
from .filters import RegistrationFilter


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    list:     GET    /api/v1/registrations/
    create:   POST   /api/v1/registrations/
    retrieve: GET    /api/v1/registrations/{id}/
    update:   PUT    /api/v1/registrations/{id}/
    partial:  PATCH  /api/v1/registrations/{id}/
    destroy:  DELETE /api/v1/registrations/{id}/
    cancel:   POST   /api/v1/registrations/{id}/cancel/
    check_in: POST   /api/v1/registrations/{id}/check-in/
    by_event: GET    /api/v1/registrations/by-event/{event_id}/
    """

    queryset = Registrations.objects.select_related('event').all()
    serializer_class = RegistrationSerializer

    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class  = RegistrationFilter
    search_fields    = ['full_name', 'email', 'event__title']
    ordering_fields  = ['created_at', 'full_name', 'status']
    ordering         = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['cancel', 'destroy']:
            return RegistrationCancelSerializer
        return RegistrationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user     = self.request.user

        # Non-staff hanya lihat registrasi miliknya sendiri
        if user.is_authenticated and not user.is_staff:
            queryset = queryset.filter(email=user.email)

        return queryset

    def destroy(self, request, *args, **kwargs):
        """Soft delete — ubah status ke cancelled dan kurangi current_capacity."""
        instance = self.get_object()

        if instance.status == Registrations.STATUS_CANCELLED:
            return Response(
                {'detail': 'Registration is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=instance.event_id)
            if event.current_capacity > 0:
                event.current_capacity -= 1
                event.save(update_fields=['current_capacity'])

            instance.status = Registrations.STATUS_CANCELLED
            instance.save(update_fields=['status', 'updated_at'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        POST /api/v1/registrations/{id}/cancel/
        Sama dengan destroy tapi lewat action eksplisit.
        """
        instance = self.get_object()

        if instance.status == Registrations.STATUS_CANCELLED:
            return Response(
                {'detail': 'Registration is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            event = Event.objects.select_for_update().get(pk=instance.event_id)
            if event.current_capacity > 0:
                event.current_capacity -= 1
                event.save(update_fields=['current_capacity'])

            instance.status = Registrations.STATUS_CANCELLED
            instance.save(update_fields=['status', 'updated_at'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        instance = self.get_object()

        if instance.status != Registrations.STATUS_REGISTERED:
            return Response(
                {'detail': f"Cannot check in a registration with status '{instance.status}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RegistrationSerializer(
            instance,
            data={'status': Registrations.STATUS_CHECKED_IN},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)