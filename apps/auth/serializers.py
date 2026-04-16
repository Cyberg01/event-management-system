from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  """
  Custom JWT Token Serializer with user info in claims.

  Add custom claims to the token:
  - username
  - email
  - role
  - user_id
  """
    
  @classmethod
  def get_token(cls, user):
    """Add custom claims to the JWT token"""
    token = super().get_token(user)
        
    # Add custom claims
    token['username'] = user.username
    token['email'] = user.email
    token['role'] = user.role
    token['user_id'] = str(user.id)
        
    return token