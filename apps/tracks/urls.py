from django.urls import path
from .views import (
    listTracks,
    createTrack,
    showTrackById,
    updateTrack,
    deleteTrack
)

urlpatterns = [
    path('v1/tracks/', listTracks, name='list-tracks'),
    path('v1/tracks/create/', createTrack, name='create-track'),
    path('v1/tracks/<uuid:track_id>/', showTrackById, name='show-track'),
    path('v1/tracks/<uuid:track_id>/update/', updateTrack, name='update-track'),
    path('v1/tracks/<uuid:track_id>/delete/', deleteTrack, name='delete-track'),
]