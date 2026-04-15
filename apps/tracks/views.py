from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Track
from .serializers import TrackSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listTracks(request):
    tracks = Track.objects.all().select_related('event')
    tracks = tracks.order_by('event__event_start_time', 'name')
    serializer = TrackSerializer(tracks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTrack(request):
    """Create a new track"""
    serializer = TrackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showTrackById(request, track_id):
    """Get single track by ID"""
    try:
        track = get_object_or_404(Track, id=track_id)
        serializer = TrackSerializer(track)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Track.DoesNotExist:
        return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateTrack(request, track_id):
    """Update track"""
    try:
        track = get_object_or_404(Track, id=track_id)
        serializer = TrackSerializer(track, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Track.DoesNotExist:
        return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteTrack(request, track_id):
    """Delete track"""
    try:
        track = get_object_or_404(Track, id=track_id)
        track.delete()
        return Response({'message': 'Track deleted successfully'}, status=status.HTTP_200_OK)
    except Track.DoesNotExist:
        return Response({'error': 'Track not found'}, status=status.HTTP_404_NOT_FOUND)