from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/', include('apps.auth.urls')),
    
    # User profile endpoints
    path('api/', include('apps.users.urls')),
    
    # Event management endpoints
    path('api/', include('apps.events.urls')),
    path('api/', include('apps.venues.urls')),
    path('api/', include('apps.event_sessions.urls')),
    path('api/', include('apps.registrations.urls')),
    path('api/', include('apps.tracks.urls')),
    path('api/', include('apps.speakers.urls')),
]
