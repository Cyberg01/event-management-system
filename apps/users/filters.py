from apps.users.models import UserProfile
from django_filters import rest_framework as django_filters


class UsersFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    role = django_filters.CharFilter(field_name="role", lookup_expr="iexact")

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'role']