from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'

router = DefaultRouter()
router.register(r'v1/users', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]