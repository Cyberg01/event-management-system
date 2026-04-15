from django.urls import path
from . import views

urlpatterns = [
    path('v1/sessions', views.listSessions, name='list-sessions'),
    path('v1/sessions/create', views.createSession, name='create-session'),
    path('v1/sessions/<uuid:session_id>', views.showSessionById, name='show-session'),
    path('v1/sessions/<uuid:session_id>/update', views.updateSession, name='update-session'),
    path('v1/sessions/<uuid:session_id>/delete', views.deleteSession, name='delete-session'),
]