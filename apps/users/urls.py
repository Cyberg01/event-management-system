from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users import views

urlpatterns = [
    path('v1/auth/register', views.createUser, name='register'),
    path('v1/auth/profile', views.showUser, name='profile'),
    path('v1/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/profile/update', views.updateUser, name='profile-update'),
    path('v1/auth/profile/delete', views.deleteUser, name='profile-delete'),
]
