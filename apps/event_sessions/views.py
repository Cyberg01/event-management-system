from .serializers import SessionsSerializer
from .models import Sessions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listSessions(request):
    event_id = request.query_params.get('event_id')
    
    if event_id:
        sessions = Sessions.objects.filter(event_id=event_id).select_related('event')
    else:
        sessions = Sessions.objects.all().select_related('event')
    
    serializer = SessionsSerializer(sessions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createSession(request):
    serializer = SessionsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showSessionById(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        serializer = SessionsSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Sessions.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateSession(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        serializer = SessionsSerializer(session, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Sessions.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteSession(request, session_id):
    try:
        session = get_object_or_404(Sessions, id=session_id)
        session.delete()
        return Response({'message': 'Session deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Sessions.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)