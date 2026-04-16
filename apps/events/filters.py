import django_filters
from apps.events.models import Event


class EventFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    event_type = django_filters.CharFilter(field_name="event_type", lookup_expr="iexact")
    event_start_date = django_filters.DateTimeFilter(field_name="event_start_time", lookup_expr="gte")
    event_end_date = django_filters.DateTimeFilter(field_name="event_end_time", lookup_expr="lte")
    registration_start_date = django_filters.DateTimeFilter(field_name="registration_start_time", lookup_expr="gte")
    registration_end_date = django_filters.DateTimeFilter(field_name="registration_end_time", lookup_expr="lte")
    
    """venue filter"""
    venue_name = django_filters.CharFilter(field_name="venue__name", lookup_expr="icontains")
    venume_city = django_filters.CharFilter(field_name="venue__city", lookup_expr="icontains")
    venue_state = django_filters.CharFilter(field_name="venue__state", lookup_expr="icontains")
    venue_country = django_filters.CharFilter(field_name="venue__country", lookup_expr="icontains")

    class Meta:
        model = Event
        fields = ['creator']