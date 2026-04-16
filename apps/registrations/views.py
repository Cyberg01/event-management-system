from django_filters.rest_framework import DjangoFilterBackend
from apps.registrations.filters import RegistrationsFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from .serializers import RegistrationsSerializer
from .models import Registrations
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from apps.common.utils.responses import success_response, error_response

class RegistraionsListView(ListAPIView):
    queryset = Registrations.objects.all()
    serializer_class = RegistrationsSerializer
    permission_classes = [IsAuthenticated]

    filterset_class = RegistrationsFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['attendee__username', 'event__title', 'session__title', 'status']
    ordering_fields = ['-created_at']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRegistration(request):
    """Create a new registration - auto-assign authenticated user as attendee"""
    # Auto-assign authenticated user as attendee
    data = request.data.copy()
    data['attendee'] = request.user.id
    
    serializer = RegistrationsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return success_response(serializer.data, message="Registration created successfully", status=status.HTTP_201_CREATED)
    return error_response("Registration creation failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showRegistrationById(request, registration_id):
    """Get single registration by ID"""
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        serializer = RegistrationsSerializer(registration)
        return success_response(serializer.data, message="Registration retrieved successfully")
    except Registrations.DoesNotExist:
        return error_response("Registration not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateRegistration(request, registration_id):
    """Update registration"""
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        serializer = RegistrationsSerializer(registration, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="Registration updated successfully")
        return error_response("Registration update failed", errors=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Registrations.DoesNotExist:
        return error_response("Registration not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteRegistration(request, registration_id):
    """Delete registration"""
    try:
        registration = get_object_or_404(Registrations, id=registration_id)
        registration.delete()
        return success_response(None, message="Registration deleted successfully")
    except Registrations.DoesNotExist:
        return error_response("Registration not found", status=status.HTTP_404_NOT_FOUND)