from django.urls import path
from . import views

urlpatterns = [
    path('v1/events/create/', views.createEvent, name='create_event'),
    path('v1/events/<int:event_id>/', views.showEventById, name='show_event'),
    path('v1/events/<int:event_id>/update/', views.updateEvent, name='update_event'),
    path('v1/events/<int:event_id>/delete/', views.deleteEvent, name='delete_event'),
]