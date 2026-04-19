from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Event
from .serializers import EventSerializer
from .filters import EventFilter
from apps.common.utils.responses import success_response, error_response
from apps.common.utils.permissions import IsEventCreatorOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    """
    Django ViewSet for CRUD operations on Event model.
    
    Provides:
    - List all events (GET /api/v1/events/)
    - Create new event (POST /api/v1/events/)
    - Retrieve event detail (GET /api/v1/events/{id}/)
    - Update event (PUT/PATCH /api/v1/events/{id}/)
    - Delete event (DELETE /api/v1/events/{id}/)
    """
    
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    # Filtering and searching configuration
    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['event_start_time', 'capacity', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Set permission based on action.
        - list, retrieve: IsAuthenticated
        - create: IsAuthenticated
        - update, partial_update, destroy: IsEventCreatorOrReadOnly
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsEventCreatorOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Create a new event.
        - Automatically set creator as current user
        - Perform validation through serializer
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Set the creator to the authenticated user
            serializer.save(creator=request.user)
            return success_response(
                serializer.data,
                message="Event created successfully",
                status=status.HTTP_201_CREATED
            )
        
        return error_response(
            "Validation error occurred",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(
                serializer.data,
                message="Event retrieved successfully"
            )
        except Event.DoesNotExist:
            return error_response(
                "Event not found",
                status=status.HTTP_404_NOT_FOUND
            )

    # def update(self, request, *args, **kwargs):
    #     """
    #     Update an existing event (full update).
    #     - User must be the event creator
    #     - All required fields must be provided
    #     """
    #     try:
    #         instance = self.get_object()
            
    #         # Check if user is the creator
    #         if instance.creator != request.user:
    #             return error_response(
    #                 "You don't have permission to update this event",
    #                 status=status.HTTP_403_FORBIDDEN
    #             )
            
    #         serializer = self.get_serializer(instance, data=request.data, partial=False)
            
    #         if serializer.is_valid():
    #             serializer.save()
    #             return success_response(
    #                 serializer.data,
    #                 message="Event updated successfully"
    #             )
            
    #         return error_response(
    #             "Validation error occurred",
    #             errors=serializer.errors,
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     except Event.DoesNotExist:
    #         return error_response(
    #             "Event not found",
    #             status=status.HTTP_404_NOT_FOUND
    #         )

    def update(self, request, *args, **kwargs):
        """
        Partial update of an event.
        - User must be the event creator
        - Only specified fields are updated
        """
        try:
            instance = self.get_object()
            
            # Check if user is the creator
            if instance.creator != request.user:
                return error_response(
                    "You don't have permission to update this event",
                    status=status.HTTP_403_FORBIDDEN
                )
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    serializer.data,
                    message="Event updated successfully"
                )
            
            return error_response(
                "Validation error occurred",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Event.DoesNotExist:
            return error_response(
                "Event not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an event.
        - User must be the event creator
        - Cannot delete event if it has active registrations
        """
        try:
            instance = self.get_object()
            
            # Check if user is the creator
            if instance.creator != request.user:
                return error_response(
                    "You don't have permission to delete this event",
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if event has registrations
            if instance.registrations.exists():
                return error_response(
                    "Cannot delete event with existing registrations",
                    status=status.HTTP_409_CONFLICT
                )
            
            instance.delete()
            return success_response(
                None,
                message="Event deleted successfully",
                status=status.HTTP_204_NO_CONTENT
            )
        except Event.DoesNotExist:
            return error_response(
                "Event not found",
                status=status.HTTP_404_NOT_FOUND
            )