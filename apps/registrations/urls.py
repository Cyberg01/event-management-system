from django.urls import path
from . import views

urlpatterns = [
    path('v1/registrations', views.RegistraionsListView.as_view(), name='list-registrations'),
    path('v1/registrations/create', views.createRegistration, name='create-registration'),
    path('v1/registrations/<uuid:registration_id>', views.showRegistrationById, name='show-registration'),
    path('v1/registrations/<uuid:registration_id>/update', views.updateRegistration, name='update-registration'),
    path('v1/registrations/<uuid:registration_id>/delete', views.deleteRegistration, name='delete-registration'),
]