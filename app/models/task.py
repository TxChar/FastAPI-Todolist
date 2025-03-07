import datetime
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    ListField,
    ReferenceField,
    BooleanField,
)
from .subtask import SubTask
from .object_id_validate import PyObjectId
from typing import Optional
from pydantic import Field


class Task(Document):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name = StringField(required=True, max_length=200)
    status = StringField(
        required=True, choices=["Pending", "In Progress", "Done"], default="Pending"
    )
    is_deleted = BooleanField(default=False, choices=[True, False])
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    expected_date = DateTimeField()

    subtasks = ListField(ReferenceField(SubTask, reverse_delete_rule=2))

    meta = {"collection": "tasks"}
