from django.urls import path
from . import views

urlpatterns = [
    path('v1/sessions/', views.listSessions, name='list_sessions'),
    path('v1/sessions/create/', views.createSession, name='create_session'),
    path('v1/sessions/<uuid:session_id>/', views.showSessionById, name='show_session'),
    path('v1/sessions/<uuid:session_id>/update/', views.updateSession, name='update_session'),
    path('v1/sessions/<uuid:session_id>/delete/', views.deleteSession, name='delete_session'),
]