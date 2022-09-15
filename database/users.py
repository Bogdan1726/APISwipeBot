from settings.config import DB_PORT, DB_HOST, DB_NAME
from mongoengine import Document, disconnect, fields
from mongoengine import connect


class User(Document):
    user = fields.IntField(required=True)
    chat = fields.IntField(required=True)
    token = fields.StringField(required=True)
    is_authenticated = fields.BooleanField(default=False)


connect(db=DB_NAME, host=DB_HOST, port=DB_PORT)
disconnect()
