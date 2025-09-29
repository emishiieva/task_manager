from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from app.utils.helpers import format_datetime


class TaskStatusEnum(str, Enum):
    todo = "To Do"
    in_progress = "In Progress"
    done = "Done"


class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[TaskStatusEnum] = TaskStatusEnum.todo


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatusEnum]


class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatusEnum
    created_at: str
    model_config = {"from_attributes": True}

    @field_validator("created_at", mode="before")
    def format_created_at(cls, value):
        if isinstance(value, datetime):
            return format_datetime(value)
        return value
