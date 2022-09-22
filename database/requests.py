from mongoengine import connect, disconnect

from database.users import User
from settings.config import DB_PORT, DB_HOST, DB_NAME

connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)


def set_tokens(data, user_id):
    user = User.objects(user=user_id)
    if user:
        user.update_one(token=data.get('access_token'))
        user.update_one(refresh_token=data.get('refresh_token'))
        user.update_one(is_authenticated=True)
    else:
        user = User(
            user=user_id,
            token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            is_authenticated=True,
        )
        user.save()


def update_token(token, user_id):
    user = User.objects(user=user_id)
    if user:
        user.update_one(token=token)


def logout(user_id):
    user = User.objects(user=user_id)
    if user:
        user.update_one(is_authenticated=False)


def is_authenticated(user_id):
    user = User.objects(user=user_id).first()
    if user:
        if user.is_authenticated is True:
            return True
    return False


def get_token(user_id):
    user = User.objects(user=user_id).first()
    return user.token


def get_refresh_token(user_id) -> str:
    user = User.objects(user=user_id).first()
    return user.refresh_token
