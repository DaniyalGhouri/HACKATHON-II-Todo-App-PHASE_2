from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from src.auth.dependencies import get_current_user
from src.db import get_session
from src.models.task import Task, TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import create_task, get_tasks_by_user, get_task_by_id_and_user, update_task, delete_task
from typing import Optional

router = APIRouter()

# Helper to check uniqueness (restored from previous service logic pattern)
def _check_unique_title(session: Session, user_id: str, title: str, exclude_id: Optional[int] = None):
    query = select(Task).where(Task.user_id == user_id, Task.title == title)
    if exclude_id:
        query = query.where(Task.id != exclude_id)
    if session.exec(query).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A task with this title already exists for this user."
        )

@router.post("/api/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["id"]
    _check_unique_title(session, user_id, task.title)
    
    return create_task(session=session, task=task, user_id=user_id)


@router.get("/api/tasks", response_model=list[TaskRead])
def list_tasks_endpoint(
    status: str = Query("all", regex="^(all|pending|completed)$"),
    sort: str = Query("created", regex="^(created|title)$"),
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["id"]
    return get_tasks_by_user(session=session, user_id=user_id, status_filter=status, sort_by=sort)

@router.patch("/api/tasks/{task_id}", response_model=TaskRead)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["id"]
    
    # Check emptiness
    if task_update.title is not None and not task_update.title:
        raise HTTPException(status_code=400, detail="Task title cannot be empty.")

    # Check uniqueness if title changes
    if task_update.title:
        _check_unique_title(session, user_id, task_update.title, exclude_id=task_id)
    
    db_task = update_task(session=session, task_id=task_id, user_id=user_id, task_update=task_update)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return db_task


@router.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user_id = current_user["id"]
    if not delete_task(session=session, task_id=task_id, user_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
