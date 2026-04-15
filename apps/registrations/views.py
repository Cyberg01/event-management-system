from .serializers import RegistrationsSerializer
from .models import Registrations
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRegistration(request):
    serializer = RegistrationsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showRegistrationById(request, registration_id):
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        serializer = RegistrationsSerializer(registration)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Registrations.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateRegistration(request, registration_id):
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        serializer = RegistrationsSerializer(registration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Registrations.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteRegistration(request, registration_id):
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        registration.delete()
        return Response({'message': 'Registration deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Registrations.DoesNotExist:
        return Response({'error': 'Registration not found'}, status=status.HTTP_404_NOT_FOUND)