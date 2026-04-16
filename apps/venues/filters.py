import django_filters
from .models import Venue


class VenueFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
  city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
  state = django_filters.CharFilter(field_name="state", lookup_expr="icontains")
  country = django_filters.CharFilter(field_name="country", lookup_expr="icontains")
  capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr="gte")

  class Meta:
    model = Venue
    fields = {
      'name': ['iexact', 'icontains'],
      'city': ['iexact', 'icontains'],
      'state': ['iexact', 'icontains'],
      'country': ['iexact', 'icontains'],
      'capacity': ['gte', 'lte', 'exact'],
    }