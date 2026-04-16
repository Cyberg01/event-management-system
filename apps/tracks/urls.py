from django.urls import path
from .views import (
    ListTracksView,
    createTrack,
    showTrackById,
    updateTrack,
    deleteTrack
)

urlpatterns = [
    path('v1/tracks', ListTracksView.as_view(), name='list-tracks'),
    path('v1/tracks/create', createTrack, name='create-track'),
    path('v1/tracks/<uuid:track_id>', showTrackById, name='show-track'),
    path('v1/tracks/<uuid:track_id>/update', updateTrack, name='update-track'),
    path('v1/tracks/<uuid:track_id>/delete', deleteTrack, name='delete-track'),
]