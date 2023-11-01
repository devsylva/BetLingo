from .serializers import *
from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash

# Create your views here.

# POST: returns token pair after login
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# POST: handles user registration

@api_view(["POST"])
@permission_classes([AllowAny])
def signUp(request):
    """
    Create a new User
    """
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(owner=request.user)
            user.is_active = True
            user.save()
        else:
            return Response({
                "status": "500",
                "message": "invalid data provided",
                "data":serializer.errors
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        data = {
            "success": True,
            "message": "registration successful",
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)


# POST: handles logging out a user
# requires authentication to perform this func
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# POST: handles changing of password
# requires authentication to perform this func
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    def put(self, request):
        user = request.user  # Assuming you have authentication set up
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)