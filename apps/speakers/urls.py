from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'speakers'

router = DefaultRouter()
router.register(r'v1/speakers', views.SpeakerViewSet, basename='speaker')

urlpatterns = [
    path('', include(router.urls)),
]