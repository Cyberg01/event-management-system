from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Track
from .serializers import TrackSerializer
from apps.common.utils.responses import success_response, error_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listTracks(request):
    """List all tracks, optionally filtered by event"""
    event_id = request.query_params.get('event')
    
    if event_id:
        tracks = Track.objects.filter(event__id=event_id).select_related('event')
    else:
        tracks = Track.objects.all().select_related('event')
    
    tracks = tracks.order_by('event__event_start_time', 'name')
    serializer = TrackSerializer(tracks, many=True)
    return success_response(serializer.data, message="Tracks retrieved successfully")


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