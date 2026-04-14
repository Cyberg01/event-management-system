from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import UserProfile
from apps.users.serializers import UserRegisterSerializer, UserDetailSerializer

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
def showUser(request):
    """ API for showing user profile details"""
    """GET /api/v1/auth/profile/"""
    if request.method == 'GET':
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)