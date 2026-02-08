from sqlmodel import Session, select, col
from src.models.task import Task, TaskCreate, TaskUpdate
from typing import Optional
from datetime import datetime

def _check_task_title_uniqueness(*, session: Session, user_id: str, title: str, exclude_task_id: Optional[int] = None) -> bool:
    """
    Checks if a task title is unique for a given user, optionally excluding a task by its ID.
    """
    query = select(Task).where(Task.user_id == user_id, Task.title == title)
    if exclude_task_id:
        query = query.where(Task.id != exclude_task_id)
    existing_task = session.exec(query).first()
    return existing_task is None

def create_task(*, session: Session, task: TaskCreate, user_id: str) -> Task:
    db_task = Task.model_validate(task, update={"user_id": user_id})
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_tasks_by_user(*, session: Session, user_id: str, status_filter: str = "all", sort_by: str = "created") -> list[Task]:
    query = select(Task).where(Task.user_id == user_id)

    # Filter by status
    if status_filter == "completed":
        query = query.where(Task.is_completed == True)
    elif status_filter == "pending":
        query = query.where(Task.is_completed == False)
    
    # Sort
    if sort_by == "title":
        query = query.order_by(Task.title)
    else: # default to created
        query = query.order_by(Task.created_at)

    tasks = session.exec(query).all()
    return tasks

def get_task_by_id_and_user(*, session: Session, task_id: int, user_id: str) -> Optional[Task]:
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    return task

def update_task(*, session: Session, task_id: int, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    db_task = get_task_by_id_and_user(session=session, task_id=task_id, user_id=user_id)
    if not db_task:
        return None
    
    update_data = task_update.model_dump(exclude_unset=True)

    # Handle 'completed' field mapping if it comes from frontend
    if "completed" in update_data:
        update_data["is_completed"] = update_data.pop("completed")

    # Check for title uniqueness if title is being updated
    if "title" in update_data and update_data["title"] != db_task.title:
         existing = session.exec(select(Task).where(Task.user_id == user_id, Task.title == update_data["title"], Task.id != task_id)).first()
         if existing:
             pass

    # Apply updates
    for key, value in update_data.items():
        if hasattr(db_task, key):
            setattr(db_task, key, value)
    
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(*, session: Session, task_id: int, user_id: str) -> bool:
    task = get_task_by_id_and_user(session=session, task_id=task_id, user_id=user_id)
    if not task:
        return False
    session.delete(task)
    session.commit()
    return True
