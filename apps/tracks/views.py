from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.tracks.filters import TrackFilter
from .models import Track
from .serializers import TrackSerializer
from apps.common.utils.responses import success_response, error_response


class ListTracksView(ListAPIView):
    queryset = Track.objects.all().order_by('-created_at')
    serializer_class = TrackSerializer

    permission_classes = [IsAuthenticated]

    filterset_class = TrackFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['name']
    ordering_fields = ['-created_at']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTrack(request):
    """Create a new track (Admin only)"""
    serializer = TrackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, message="Track created successfully", status=status.HTTP_201_CREATED)
    return error_response("Track creation failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showTrackById(request, track_id):
    """Get single track by ID"""
    try:
        track = get_object_or_404(Track, id=track_id)
        serializer = TrackSerializer(track)
        return success_response(serializer.data, message="Track retrieved successfully")
    except Track.DoesNotExist:
        return error_response("Track not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTrack(request, track_id):
    """Update track (Admin only)"""
    try:
        track = get_object_or_404(Track, id=track_id)
        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Track updated successfully")
        return error_response("Track update failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Track.DoesNotExist:
        return error_response("Track not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTrack(request, track_id):
    """Delete track (Admin only)"""
    try:
        track = get_object_or_404(Track, id=track_id)
        track.delete()
        return success_response(None, message="Track deleted successfully")
    except Track.DoesNotExist:
        return error_response("Track not found", status=status.HTTP_404_NOT_FOUND)