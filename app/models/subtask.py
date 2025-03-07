from mongoengine import Document, StringField, DateTimeField
from .object_id_validate import PyObjectId
from typing import Optional
from pydantic import Field

import datetime


class SubTask(Document):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name = StringField(required=True, max_length=200)
    status = StringField(
        required=True, choices=["Pending", "In Progress", "Done"], default="Pending"
    )
    created_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    updated_date = DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
    expected_date = DateTimeField()

    meta = {"collection": "subtasks"}


# from pydantic import BaseModel, Field
# from typing import Optional
# from bson import ObjectId

# # สร้างตัวช่วยสำหรับ MongoDB ObjectId
# class PyObjectId(str):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return str(v)

# class SubTaskSchema(BaseModel):
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     name: str
#     status: str = Field(default="Pending", regex="^(Pending|In Progress|Done)$")

#     class Config:
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
