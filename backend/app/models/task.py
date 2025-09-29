from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from app.core.database import Base


class TaskStatusEnum(str, enum.Enum):
    todo = "To Do"
    in_progress = "In Progress"
    done = "Done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(
        Enum(TaskStatusEnum, native_enum=False),
        nullable=False,
        default=TaskStatusEnum.todo,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
