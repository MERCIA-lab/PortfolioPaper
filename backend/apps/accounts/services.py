from .models import User

def user_create(*, email: str, username: str, password: str) -> User:
    return User.objects.create_user(
        email=email,
        username=username,
        password=password
    )