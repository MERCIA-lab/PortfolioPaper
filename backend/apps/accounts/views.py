import logging

from django.conf import settings
from django.middleware.csrf import get_token
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from.serializers import UserCreateSerializer, UserLoginSerializer, UserLogoutSerializer, UserSerializer
from.services import blacklist_refresh_token, login_and_get_tokens, create_user_and_get_tokens

class CsrfTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = create_user_and_get_tokens(**serializer.validated_data)
        user = result["user"]

    
        subject = "User registered successfully!"
        message = f"Hello {user.username}! Congratulations.\nYour account is active since {timezone.now():%Y-%m-%d %H:%M}"

        try:
            send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        except Exception as e:
            logging.warning(f"Email failed {e}")

        return Response({
            "user": UserSerializer(user).data,
            "access": result["access"],
            "refresh": result["refresh"]
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = login_and_get_tokens(**serializer.validated_data)
        user = result["user"]
        response = Response({
            "user": UserSerializer(user).data,
            "access": result["access"],
            "refresh": result["refresh"],
        })
        response.set_cookie('access_token', result['access'], httponly=True, secure=request.is_secure(), samesite='Lax')
        response.set_cookie('refresh_token', result['refresh'], httponly=True, secure=request.is_secure(), samesite='Lax')
        return response

class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token and request.data:
            serializer = UserLogoutSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data['refresh']
        if refresh_token:
            try:
                blacklist_refresh_token(refresh_token)
            except AuthenticationFailed:
                logging.info("Refresh token could not be blacklisted during logout.")
        response = Response(status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)