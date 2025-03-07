from mongoengine import Document, StringField, EmailField


class User(Document):
    name = StringField(required=True, max_length=100)
    email = EmailField(required=True, unique=True)

    meta = {"collection": "users"}
