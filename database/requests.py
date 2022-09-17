from mongoengine import connect, disconnect

from database.users import User
from settings.config import DB_PORT, DB_HOST, DB_NAME

connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)


async def set_token(data, user_id):
    user = User.objects(user=user_id)
    if user:
        user.update_one(token=data.get('access_token'))
    else:
        user = User(
            user=user_id,
            chat=1,
            token=data.get('access_token'),
            is_authenticated=True,
        )
        user.save()

    for doc in User.objects():
        print(doc)


def create_user(data):
    pass


