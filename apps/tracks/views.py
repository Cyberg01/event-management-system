# views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import request, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.common.utils.permissions import IsAdminUser, IsEventCreatorOrReadOnly
from apps.common.utils.responses import success_response, error_response
from apps.tracks.filters import TrackFilter
from apps.tracks.models import Track
from apps.tracks.serializers import TrackSerializer

class TrackViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Track CRUD operations
    - List: GET /api/v1/tracks/
    - Create: POST /api/v1/tracks/
    - Retrieve: GET /api/v1/tracks/{id}/
    - Update: PUT/PATCH /api/v1/tracks/{id}/
    - Delete: DELETE /api/v1/tracks/{id}/
    """
    queryset = Track.objects.all().order_by('-created_at')
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    
    filterset_class = TrackFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def create(self, request, *args, **kwargs):
        """
        Create a new track.
        - Automatically set creator as current user
        - Perform validation through serializer
        """
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Set the creator to the authenticated user
            serializer.save(creator=str(request.user.id))
            return success_response(
                serializer.data,
                message="Track created successfully",
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
                message="Track retrieved successfully"
            )
        except Track.DoesNotExist:
            return error_response(
                "Track not found",
                status=status.HTTP_404_NOT_FOUND
            )
    

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True 
        return super().update(request, *args, **kwargs)
    
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a track.
        - User must be the track creator or an admin
        - Cannot delete track if it has active registrations
        """
        try:
            instance = self.get_object()

            print("Logger", {request})

            is_admin = request.user.role.lower() == 'admin' or request.user.is_superuser
            
            # Check if user is the creator or admin
            if instance.creator != str(request.user.id) and not is_admin:
                return error_response(
                    "You don't have permission to delete this track",
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Check if track has registrations
            # if instance.registrations.exists():
            #     return error_response(
            #         "Cannot delete track with existing registrations",
            #         status=status.HTTP_409_CONFLICT
            #     )
            
            instance.delete()
            return success_response(
                None,
                message="Track deleted successfully",
                status=status.HTTP_204_NO_CONTENT
            )
        except Track.DoesNotExist:
            return error_response(
                "Track not found",
                status=status.HTTP_404_NOT_FOUND
            )