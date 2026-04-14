from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.venues.serializers import VenueSerializer
from .models import Venue

class VenueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return Venue.objects.get(pk=pk)

    def get(self, request, pk=None):
        if pk:
            venue = self.get_object(pk)
            serializer = VenueSerializer(venue)
            return Response(serializer.data)

        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VenueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        venue = self.get_object(pk)
        serializer = VenueSerializer(venue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        venue = self.get_object(pk)
        venue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)