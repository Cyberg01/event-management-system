from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Speaker
from .serializers import SpeakerSerializer
from apps.common.utils.responses import success_response, error_response
from apps.common.utils.permissions import IsCreatorOrReadOnly


class SpeakerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Speaker model.
    
    Endpoints:
    - GET    /api/v1/speakers/          - List all speakers
    - POST   /api/v1/speakers/          - Create new speaker
    - GET    /api/v1/speakers/{id}/     - Retrieve speaker detail
    - PUT    /api/v1/speakers/{id}/     - Update speaker
    - DELETE /api/v1/speakers/{id}/     - Delete speaker
    """
    
    queryset = Speaker.objects.all().prefetch_related('sessions').order_by('-created_at')
    serializer_class = SpeakerSerializer
    permission_classes = [IsAuthenticated]
    
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options']
    
    # Filtering and searching configuration
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'email', 'title', 'company']
    ordering_fields = ['full_name', 'company', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Apply permissions based on action.
        - list, retrieve, create: IsAuthenticated
        - partial_update, destroy: IsAuthenticated + IsCreatorOrReadOnly
        """
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Create a new speaker"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(creator=request.user.id)
            return success_response(
                serializer.data,
                message="Speaker created successfully",
                status=status.HTTP_201_CREATED
            )
        
        return error_response(
            "Validation error occurred",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        """List all speakers with filtering and pagination"""
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            serializer.data,
            message="Speakers retrieved successfully"
        )

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single speaker by ID"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return success_response(
                serializer.data,
                message="Speaker retrieved successfully"
            )
        except Speaker.DoesNotExist:
            return error_response(
                "Speaker not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, *args, **kwargs):
        """Update speaker (PUT only)"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    serializer.data,
                    message="Speaker updated successfully"
                )
            
            return error_response(
                "Validation error occurred",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Speaker.DoesNotExist:
            return error_response(
                "Speaker not found",
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, *args, **kwargs):
        """Delete a speaker"""
        try:
            instance = self.get_object()
            
            # Check if speaker has active sessions
            if instance.sessions.exists():
                return error_response(
                    "Cannot delete speaker with active sessions",
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            instance.delete()
            return success_response(
                None,
                message="Speaker deleted successfully",
                status=status.HTTP_200_OK
            )
        except Speaker.DoesNotExist:
            return error_response(
                "Speaker not found",
                status=status.HTTP_404_NOT_FOUND
            )