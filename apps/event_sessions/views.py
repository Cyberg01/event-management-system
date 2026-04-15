from .serializers import SessionsSerializer
from .models import Sessions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.common.utils.responses import success_response, error_response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listSessions(request):
    event_id = request.query_params.get('event_id')
    
    if event_id:
        sessions = Sessions.objects.filter(event_id=event_id).select_related('event', 'track')
    else:
        sessions = Sessions.objects.all().select_related('event', 'track')
    
    sessions = sessions.order_by('start_time')
    serializer = SessionsSerializer(sessions, many=True)
    return success_response(serializer.data, message="Sessions retrieved successfully")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSession(request):
    serializer = SessionsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, message="Session created successfully", status=status.HTTP_201_CREATED)
    return error_response("Session creation failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showSessionById(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        serializer = SessionsSerializer(session)
        return success_response(serializer.data, message="Session retrieved successfully")
    except Sessions.DoesNotExist:
        return error_response("Session not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateSession(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        serializer = SessionsSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Session updated successfully")
        return error_response("Session update failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Sessions.DoesNotExist:
        return error_response("Session not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSession(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        session.delete()
        return success_response(None, message="Session deleted successfully")
    except Sessions.DoesNotExist:
        return error_response("Session not found", status=status.HTTP_404_NOT_FOUND)