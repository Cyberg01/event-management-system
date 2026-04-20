import django_filters
from apps.registrations.models import Registrations


class RegistrationFilter(django_filters.FilterSet):
    event       = django_filters.UUIDFilter(field_name='event__id')
    event_title = django_filters.CharFilter(
        field_name='event__title',
        lookup_expr='icontains'
    )
    status    = django_filters.ChoiceFilter(choices=Registrations.STATUS_CHOICES)
    email     = django_filters.CharFilter(lookup_expr='icontains')
    full_name = django_filters.CharFilter(lookup_expr='icontains')
    organization = django_filters.CharFilter(lookup_expr='icontains')

    registered_after  = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    registered_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model  = Registrations
        fields = [
            'event', 'event_title', 'status',
            'email', 'full_name', 'organization',
            'registered_after', 'registered_before',
        ]