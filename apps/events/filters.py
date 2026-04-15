import django_filters
from apps.events.models import Event


class EventFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    event_type = django_filters.CharFilter(field_name="event_type", lookup_expr="iexact")
    start_date = django_filters.DateTimeFilter(field_name="start_date", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="end_date", lookup_expr="lte")
    capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr="gte")

    class Meta:
        model = Event
        fields = ['creator']