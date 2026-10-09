from .models import User

def user_get_by_email(*, email: str) -> User | None:
    return User.objects.filter(email=email).first()

def user_list():
    return User.objects.all()