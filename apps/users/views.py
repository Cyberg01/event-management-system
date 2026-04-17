from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from apps.users.filters import UsersFilter
from apps.users.models import UserProfile
from apps.users.serializers import (
    UserDetailSerializer,
    UserUpdateSerializer,
    CreateUserSerializer,
)
from apps.common.utils.permissions import IsSuperUser
from apps.common.utils.responses import success_response, error_response


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticated, IsSuperUser]

    filterset_class = UsersFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email', 'username']
    ordering_fields = ['created_at', 'username']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                UserDetailSerializer(user).data,
                message="User created successfully",
                status=status.HTTP_201_CREATED
            )
        return error_response(
            message="User creation failed",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.get_queryset())
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            serializer.data,
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(
            serializer.data,
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            return success_response(
                UserDetailSerializer(instance).data,
            )
        return error_response(
            message="Update failed",
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object()
        instance.delete()
        return success_response(
            {},
            status=status.HTTP_204_NO_CONTENT
        )