from django.urls import path
from . import views

urlpatterns = [
    path('v1/venues/', views.VenueAPIView.as_view(), name='venue_list'),
    path('v1/venues/<uuid:pk>/', views.VenueAPIView.as_view(), name='venue_detail'),
]