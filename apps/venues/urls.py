from django.urls import path
from . import views

urlpatterns = [
    path('v1/venues', views.VenueListView.as_view(), name='list-venues'),
    path('v1/venues/create', views.createVenue, name='create-venue'),
    path('v1/venues/<uuid:venue_id>', views.showVenueById, name='show-venue'),
    path('v1/venues/<uuid:venue_id>/update', views.updateVenue, name='update-venue'),
    path('v1/venues/<uuid:venue_id>/delete', views.deleteVenue, name='delete-venue'),
]