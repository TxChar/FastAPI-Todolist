import datetime
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
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
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    expected_date = DateTimeField()

    # ใช้ ReferenceField เพื่อเชื่อมโยงกับ Sub-Task (1 Main Task มีหลาย Sub-Tasks)
    subtasks = ListField(ReferenceField(SubTask, reverse_delete_rule=2))

    meta = {"collection": "tasks"}
