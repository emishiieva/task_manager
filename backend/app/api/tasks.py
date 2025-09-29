from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.database import get_db
from app.crud import create_task, get_tasks, get_task_by_id, update_task, delete_task

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# ---------------- CREATE ----------------
@router.post("/", response_model=TaskRead)
def api_create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = create_task(db, payload)
    return TaskRead.model_validate(task)


# ---------------- READ (list) ----------------
@router.get("/", response_model=List[TaskRead])
def api_list_tasks(
    status: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * per_page
    tasks = get_tasks(
        db, skip=skip, limit=per_page, status=status, sort_order=sort_order
    )
    return [TaskRead.model_validate(task) for task in tasks]


# ---------------- READ (single) ----------------
@router.get("/{task_id}", response_model=TaskRead)
def api_get_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.model_validate(task)


# ---------------- UPDATE ----------------
@router.put("/{task_id}", response_model=TaskRead)
def api_update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    updated = update_task(db, task_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskRead.model_validate(updated)


# ---------------- DELETE ----------------
@router.delete("/{task_id}", status_code=204)
def api_delete_task(task_id: int, db: Session = Depends(get_db)):
    success = delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
