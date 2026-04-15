from .serializers import EventSerializer
from .models import Event
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.common.utils.responses import success_response, error_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listEvents(request):
    events = Event.objects.all().select_related('venue', 'creator').order_by('-created_at')
    serializer = EventSerializer(events, many=True)
    return success_response(serializer.data, message="Events retrieved successfully")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createEvent(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        return success_response(serializer.data, message="Event created successfully", status=status.HTTP_201_CREATED)
    return error_response("Event creation failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showEventById(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event)
        return success_response(serializer.data, message="Event retrieved successfully")
    except Event.DoesNotExist:
        return error_response("Event not found", status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateEvent(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Event updated successfully")
        return error_response("Event update failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Event.DoesNotExist:
        return error_response("Event not found", status=status.HTTP_404_NOT_FOUND)

    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteEvent(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return success_response(None, message="Event deleted successfully")
    except Event.DoesNotExist:
        return error_response("Event not found", status=status.HTTP_404_NOT_FOUND) 