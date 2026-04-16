from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.auth.serializers import MyTokenObtainPairSerializer
from apps.common.utils.responses import success_response, error_response


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View JWT token obtain custom dengan MyTokenObtainPairSerializer.

    POST /api/v1/auth/login

    Request:
    {
        "username": "john_doe",
        "password": "SecurePass123!"
    }

    Response (200):
    {
        "refresh": "refresh_token",
        "access": "access_token"
    }
    """
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Wrapper untuk JWT token refresh view.

    POST /api/v1/auth/refresh

    Request:
    {
        "refresh": "refresh_token"
    }

    Response (200):
    {
        "access": "new_access_token"
    }
    """

    pass


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """ 
    Endpoint logout (simple version). 

    POST /api/v1/auth/logout 

    Authorization: Bearer access_token 

    Responses (200): 
    { 
    "state": true, 
    "message": "Logout successful", 
    "results": {} 
    } 

    Note: Token blacklist implementation may be added in the future. 
    """
    try:
        return success_response(
            {},
            message="Logout successful. Token invalidated on client-side.",
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return error_response(
            message=f"Logout error: {str(e)}", status=status.HTTP_400_BAD_REQUEST
        )
