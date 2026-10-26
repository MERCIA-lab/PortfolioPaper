from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User

def create_user_and_get_tokens(*, email: str, username: str, password: str):
    user = User.objects.create_user(
        email=email,
        username=username,
        password=password
    )
    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

def login_and_get_tokens(*, email: str, password: str):
    user = authenticate(email=email, password=password)
    if not user:
        raise AuthenticationFailed("Invalid credentials")
    refresh = RefreshToken.for_user(user)
    return {
        "user": user,
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def blacklist_refresh_token(refresh_token:str):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except TokenError:
        raise AuthenticationFailed('Invalid token')