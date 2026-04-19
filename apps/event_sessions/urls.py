from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'sessions'

router = DefaultRouter()
router.register(r'v1/sessions', views.SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]