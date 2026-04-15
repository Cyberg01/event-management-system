from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Venue
from .serializers import VenueSerializer
from apps.common.utils.responses import success_response, error_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listVenues(request):
    """List all venues"""
    venues = Venue.objects.all().order_by('name')
    serializer = VenueSerializer(venues, many=True)
    return success_response(serializer.data, message="Venues retrieved successfully")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createVenue(request):
    """Create a new venue (Admin only)"""
    serializer = VenueSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, message="Venue created successfully", status=status.HTTP_201_CREATED)
    return error_response("Venue creation failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showVenueById(request, venue_id):
    """Get single venue by ID"""
    try:
        venue = get_object_or_404(Venue, id=venue_id)
        serializer = VenueSerializer(venue)
        return success_response(serializer.data, message="Venue retrieved successfully")
    except Venue.DoesNotExist:
        return error_response("Venue not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateVenue(request, venue_id):
    """Update venue (Admin only)"""
    try:
        venue = get_object_or_404(Venue, id=venue_id)
        serializer = VenueSerializer(venue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Venue updated successfully")
        return error_response("Venue update failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Venue.DoesNotExist:
        return error_response("Venue not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteVenue(request, venue_id):
    """Delete venue (Admin only)"""
    try:
        venue = get_object_or_404(Venue, id=venue_id)
        venue.delete()
        return success_response(None, message="Venue deleted successfully")
    except Venue.DoesNotExist:
        return error_response("Venue not found", status=status.HTTP_404_NOT_FOUND)