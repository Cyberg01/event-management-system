import django_filters
from .models import Track


class TrackFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

  class Meta:
    model = Track
    fields = {
      'name': ['iexact', 'icontains'],
    }