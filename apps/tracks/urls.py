from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet

router = DefaultRouter()
router.register(r'v1/tracks', TrackViewSet, basename='track')

urlpatterns = [
    path('', include(router.urls)),
]