from mongoengine import Document, fields
from mongoengine import connect, disconnect
from settings.config import DB_PORT, DB_HOST, DB_NAME
from mongoengine.context_managers import switch_db

connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)


class User(Document):
    user = fields.IntField(required=True)
    chat = fields.IntField(required=True)
    token = fields.StringField(required=True)
    is_authenticated = fields.BooleanField(default=False)


