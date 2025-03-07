from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SubTaskBase(BaseModel):
    name: str
    status: str = Field(default="Pending", pattern="^(Pending|In Progress|Done)$")
    expected_date: Optional[datetime | None] = None


class SubTaskCreate(SubTaskBase):
    pass


class SubTaskResponse(SubTaskBase):
    id: str

    class Config:
        from_attributes = True


class MainTaskBase(BaseModel):
    name: str
    status: str = Field(default="Pending", pattern="^(Pending|In Progress|Done)$")
    expected_date: Optional[datetime] = None


class MainTaskCreate(MainTaskBase):
    sub_tasks: List[SubTaskCreate] = []


class MainTaskResponse(MainTaskBase):
    id: str
    sub_tasks: List[SubTaskResponse] = []

    class Config:
        from_attributes = True
