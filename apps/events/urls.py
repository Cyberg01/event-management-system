from django.urls import path
from . import views

urlpatterns = [
    path('v1/events', views.listEvents, name='list-events'),
    path('v1/events/create', views.createEvent, name='create-event'),
    path('v1/events/<uuid:event_id>', views.showEventById, name='show-event'),
    path('v1/events/<uuid:event_id>/update', views.updateEvent, name='update-event'),
    path('v1/events/<uuid:event_id>/delete', views.deleteEvent, name='delete-event'),
]