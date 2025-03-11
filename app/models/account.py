import datetime
from mongoengine import Document, StringField, DateTimeField


class Account(Document):
    display_name = StringField(required=True, max_length=100)
    role = StringField(required=True, choices=["user", "admin"], default="user")
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))

    meta = {"collection": "accounts"}
