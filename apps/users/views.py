from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserProfile
from apps.users.serializers import UserRegisterSerializer, UserDetailSerializer, UserUpdateSerializer

# JWT Token Generator Helper
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def createUser(request):
    """ API for user registration"""
    """POST /api/v1/auth/register/"""

    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'user': UserDetailSerializer(user).data,
                'tokens': tokens,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def showUser(request):
    """ API for showing user profile details"""
    """GET /api/v1/auth/profile/"""
    if request.method == 'GET':
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    """ API for updating user profile details (except password)"""
    """PUT /api/v1/auth/profile/"""
    if request.method == 'PUT':
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    """ API for deleting user profile"""
    """DELETE /api/v1/auth/profile/"""
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)