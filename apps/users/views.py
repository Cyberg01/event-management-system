from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserProfile
from apps.users.serializers import UserRegisterSerializer, UserDetailSerializer, UserUpdateSerializer
from apps.common.utils.responses import success_response, error_response

# JWT Token Generator Helper
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return success_response(
                {
                    'user': UserDetailSerializer(user).data,
                    'refresh': tokens['refresh'],
                    'access': tokens['access']
                },
                message='User registered successfully',
                status=status.HTTP_201_CREATED
            )
        return error_response(
            message='Registration failed',
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showUser(request):
    if request.method == 'GET':
        user = request.user
        serializer = UserDetailSerializer(user)
        return success_response(serializer.data, message='User profile retrieved successfully')
    return error_response(message='Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    if request.method == 'PUT':
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='User updated successfully')
        return error_response(
            message='Update failed',
            errors=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    return error_response(message='Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return success_response({}, message='User deleted successfully', status=status.HTTP_204_NO_CONTENT)
    return error_response(message='Method not allowed', status=status.HTTP_405_METHOD_NOT_ALLOWED)