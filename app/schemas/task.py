from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .subtask import SubTaskCreate, SubTaskResponse


class TaskBase(BaseModel):
    name: str
    status: str = Field(default="Pending", pattern="^(Pending|In Progress|Done)$")
    expected_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    subtasks: List[SubTaskCreate] = []


class TaskResponse(TaskBase):
    id: str
    subtasks: List[SubTaskResponse] = []

    class Config:
        from_attributes = True


class UpdateTaskStatus(BaseModel):
    status: str = Field(default="Pending", pattern="^(Pending|In Progress|Done)$")
