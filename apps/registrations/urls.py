from rest_framework.routers import DefaultRouter
from .views import RegistrationViewSet
from django.urls import path, include

app_name = 'registrations'

router = DefaultRouter()
router.register(r'v1/registrations', RegistrationViewSet, basename='registration')

urlpatterns = [
    path('', include(router.urls)),
]