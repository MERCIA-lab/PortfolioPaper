
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreateSerializer, UserLoginSerializer, UserLogoutSerializer, UserSerializer
from .services import blacklist_refresh_token, login_user_and_get_tokens


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(**serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, tokens = login_user_and_get_tokens(**serializer.validated_data) # type: ignore
        response = Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=tokens['access'],
            httponly=True,
            secure=True,
            samesite='None',
        )
        response.set_cookie(
            key='refresh_token',
            value=tokens['refresh'],
            httponly=True,
            secure=True,
            samesite='None',
        )
        return Response({
            "user": UserSerializer(user).data,
            **tokens
        })


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blacklist_refresh_token(serializer.validated_data['refresh']) # type: ignore
        return Response({
            "detail": "Logged out"
        }, status=status.HTTP_205_RESET_CONTENT
        )


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
