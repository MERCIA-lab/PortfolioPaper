from .models import User

def user_get_by_email(*, email: str) -> User | None:
    return User.objects.filter(email=email).first()

def user_list():
    return User.objects.all()

def get_user_by_id(*, user_id: str) -> User | None:
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

def get_user_by_email(*, email: str) -> User | None:
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None