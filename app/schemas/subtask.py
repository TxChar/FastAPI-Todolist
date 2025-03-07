from pydantic import BaseModel, Field
from typing import Optional
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


class UpdateSubTaskStatus(BaseModel):
    status: str = Field(default="Pending", pattern="^(Pending|In Progress|Done)$")


class UpdateSubTaskPartial(BaseModel):
    name: Optional[str] = None
    expected_date: Optional[datetime] = None
