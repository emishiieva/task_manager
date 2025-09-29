from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, asc, desc
from app.models.task import Task as TaskModel
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, task_in: TaskCreate) -> TaskModel:
    db_task = TaskModel(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    sort_order: str = "asc",
) -> list[TaskModel]:
    stmt = select(TaskModel)

    if status is not None:
        stmt = stmt.where(TaskModel.status == status)

    if sort_order.lower() == "desc":
        stmt = stmt.order_by(desc(TaskModel.id))
    else:
        stmt = stmt.order_by(asc(TaskModel.id))

    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def get_task_by_id(db: Session, task_id: int) -> Optional[TaskModel]:
    return db.get(TaskModel, task_id)


def update_task(db: Session, task_id: int, task_in: TaskUpdate) -> Optional[TaskModel]:
    db_task = db.get(TaskModel, task_id)
    if not db_task:
        return None

    update_data: Dict[str, Any] = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = db.get(TaskModel, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True
