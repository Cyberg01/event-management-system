from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Sessions
from .serializers import SessionsSerializer
from .filters import SessionsFilter
from apps.common.utils.responses import success_response, error_response
from apps.common.utils.permissions import IsCreatorOrReadOnly


class SessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Session model.
    
    Endpoints:
    - GET    /api/v1/sessions/          - List all sessions
    - POST   /api/v1/sessions/          - Create new session
    - GET    /api/v1/sessions/{id}/     - Retrieve session detail
    - Update  /api/v1/sessions/{id}/    - Update session (only provided fields will be updated)
    - DELETE /api/v1/sessions/{id}/     - Delete session
    
    Note: PUT is disabled, only PATCH is allowed for updates
    """
    
    queryset = Sessions.objects.all().select_related('event', 'tracks').order_by('-created_at')
    serializer_class = SessionsSerializer
    permission_classes = [IsAuthenticated]
    
    # Filtering and searching configuration
    filterset_class = SessionsFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Apply permissions based on action.
        - list, retrieve, create: IsAuthenticated
        - update, destroy: IsAuthenticated + IsCreatorOrReadOnly
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """
        Create a new session.
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Set creator to authenticated user's id
            serializer.save(creator=request.user.id)
            return success_response(
                serializer.data,
                message="Session created successfully",
                status=status.HTTP_201_CREATED
            )
        
        return error_response(
            "Validation error occurred",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        """List all sessions with filtering and pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            serializer.data,
            message="Sessions retrieved successfully"
        )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single session by ID"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(
                serializer.data,
                message="Session retrieved successfully"
            )
        except Sessions.DoesNotExist:
            return error_response(
                "Session not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """
        Only provided fields will be updated.
        Only creator can update their own sessions.
        """
        try:
            instance = self.get_object()
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    serializer.data,
                    message="Session updated successfully"
                )
            
            return error_response(
                "Validation error occurred",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Sessions.DoesNotExist:
            return error_response(
                "Session not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a session.
        Only creator can delete their own sessions.
        """
        try:
            instance = self.get_object()
            instance.delete()
            return success_response(
                None,
                message="Session deleted successfully",
                status=status.HTTP_200_OK
            )
        except Sessions.DoesNotExist:
            return error_response(
                "Session not found",
                status=status.HTTP_404_NOT_FOUND
            )