import django_filters
from .models import Registrations


class RegistrationsFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
  attendee = django_filters.CharFilter(field_name='attendee__username', lookup_expr='icontains')
  event = django_filters.CharFilter(field_name='event__title', lookup_expr='icontains')
  session = django_filters.CharFilter(field_name='session__title', lookup_expr='icontains')
  status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')

  class Meta:
    model = Registrations
    fields = ['name', 'attendee', 'event', 'session', 'status']