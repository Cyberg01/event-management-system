import django_filters
from apps.event_sessions.models import Sessions

class SessionsFilter(django_filters.FilterSet):
    tracks = django_filters.CharFilter(field_name="tracks__name", lookup_expr="icontains")
    start_time = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")
    capacity = django_filters.NumberFilter(field_name="capacity", lookup_expr="gte")

    class Meta:
        model = Sessions
        fields = ['tracks', 'start_time', 'end_time', 'capacity']