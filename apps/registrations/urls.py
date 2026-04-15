from django.urls import path
from . import views

urlpatterns = [
    # path('v1/registrations/', views.listRegistrations, name='list_registrations'),
    path('v1/registrations/create/', views.createRegistration, name='create_registration'),
    path('v1/registrations/<uuid:registration_id>/', views.showRegistrationById, name='show_registration'),
    path('v1/registrations/<uuid:registration_id>/update/', views.updateRegistration, name='update_registration'),
    path('v1/registrations/<uuid:registration_id>/delete/', views.deleteRegistration, name='delete_registration'),
]