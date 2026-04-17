from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from apps.events.filters import EventFilter
from .serializers import EventSerializer
from .models import Event
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.common.utils.responses import success_response, error_response


class EventListView(ListAPIView):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer

    permission_classes = [IsAuthenticated]

    filterset_class = EventFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'capacity']

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createEvent(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        return success_response(serializer.data, message="Event created successfully", status=status.HTTP_201_CREATED)
    return error_response("Validation Error: Field tidak sesuai", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        return error_response("Validation Error", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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