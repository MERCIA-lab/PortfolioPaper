from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .selectors import get_user_by_id,get_user_by_email

def create_user_and_get_tokens(validated_data):
    from .models import User

    user = User.objects.create_user( # type: ignore
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password']
    )
    return user, get_tokens_for_user(user)

def login_user_and_get_tokens(email, password):
    user = authenticate(email=email, password=password)
    if not user:
        if not get_user_by_email(email=email):
            raise AuthenticationFailed('User not found')
        raise AuthenticationFailed('Incorrect password')
    return user, get_tokens_for_user(user)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def blacklist_refresh_token(refresh_token:str):
    try:
        token = RefreshToken(refresh_token_str=refresh_token) # type: ignore
        token.blacklist()
        return True
    except Exception as e:
        raise AuthenticationFailed('Invalid token')