import django_filters
from .models import Sessions


class SessionsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = django_filters.CharFilter(field_name="description", lookup_expr="icontains")
    event = django_filters.UUIDFilter(field_name="event__id", lookup_expr="exact")
    event_title = django_filters.CharFilter(field_name="event__title", lookup_expr="icontains")
    
    tracks = django_filters.UUIDFilter(field_name="tracks__id", lookup_expr="exact")
    track_name = django_filters.CharFilter(field_name="tracks__name", lookup_expr="icontains")
    
    start_time_gte = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_time_lte = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="lte")
    end_time_gte = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="gte")
    end_time_lte = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="lte")
    
    creator = django_filters.CharFilter(field_name="creator", lookup_expr="iexact")

    class Meta:
        model = Sessions
        fields = [
            'title',
            'description',
            'event', 
            'event_title', 
            'tracks', 
            'track_name',
            'start_time_gte', 
            'start_time_lte', 
            'end_time_gte', 
            'end_time_lte',
            'creator'
        ]