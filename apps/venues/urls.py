from django.urls import path
from .views import (
    listVenues,
    createVenue,
    showVenueById,
    updateVenue,
    deleteVenue
)

urlpatterns = [
    path('v1/venues', listVenues, name='list-venues'),
    path('v1/venues/create', createVenue, name='create-venue'),
    path('v1/venues/<uuid:venue_id>', showVenueById, name='show-venue'),
    path('v1/venues/<uuid:venue_id>/update', updateVenue, name='update-venue'),
    path('v1/venues/<uuid:venue_id>/delete', deleteVenue, name='delete-venue'),
]