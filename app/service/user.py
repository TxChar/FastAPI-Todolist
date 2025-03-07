from app.models.user import User


def create_user(name: str, email: str):
    if User.objects(email=email):
        return None  # Email ซ้ำ
    user = User(name=name, email=email)
    user.save()
    return user


def get_users():
    return User.objects()
