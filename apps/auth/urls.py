from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    # Endpoint authenticationusing JWT
    path("v1/auth/login", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/auth/refresh", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("v1/auth/logout", views.logout_view, name="logout"),
]
