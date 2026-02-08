from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskPriority
from ..services.db import engine
from ..services.logger import log_tool_call
from .server import mcp
from agents import function_tool

@function_tool
@mcp.tool()
def add_task(user_id: str, title: str, description: Optional[str] = None, due_date: Optional[datetime] = None, priority: str = "medium") -> str:
    """
    Create a new todo task for a specific user.
    
    Args:
        user_id: The ID of the authenticated user.
        title: The title of the task.
        description: Optional detailed description.
        due_date: Optional due date/time.
        priority: Task priority (low, medium, high). Defaults to medium.
    """
    # Convert string priority to Enum
    try:
        p_enum = TaskPriority(priority.lower())
    except ValueError:
        p_enum = TaskPriority.MEDIUM

    with Session(engine) as session:
        task = Task(
            user_id=user_id, 
            title=title, 
            description=description, 
            due_date=due_date,
            priority=p_enum
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        res = f"Task created successfully with ID: {task.id}"
        log_tool_call("add_task", user_id, {"title": title, "priority": priority}, res)
        return res

@function_tool
@mcp.tool()
def list_tasks(user_id: str, completed: Optional[bool] = None) -> str:
    """
    List todo tasks for a user, optionally filtered by completion status.
    Returns task titles, IDs, status, priority, and due date.
    
    Args:
        user_id: The ID of the authenticated user.
        completed: Optional completion status filter.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if completed is not None:
            statement = statement.where(Task.is_completed == completed)
        
        tasks = session.exec(statement).all()
        if not tasks:
            res = "No tasks found."
            log_tool_call("list_tasks", user_id, {"completed": completed}, res)
            return res
        
        output = "Your tasks:\n"
        for t in tasks:
            status = "[x]" if t.is_completed else "[ ]"
            due = f", Due: {t.due_date.strftime('%Y-%m-%d %H:%M')}" if t.due_date else ""
            output += f"{t.id}. {status} {t.title} (Priority: {t.priority.value}{due})\n"
        log_tool_call("list_tasks", user_id, {"completed": completed}, "Success")
        return output

@function_tool
@mcp.tool()
def complete_task(user_id: str, task_id: int) -> str:
    """
    Mark a specific task as completed.
    
    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to complete.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            res = f"Task {task_id} not found."
            log_tool_call("complete_task", user_id, {"task_id": task_id}, res)
            return res
        
        task.is_completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        res = f"Task '{task.title}' marked as completed."
        log_tool_call("complete_task", user_id, {"task_id": task_id}, res)
        return res

@function_tool
@mcp.tool()
def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None, due_date: Optional[datetime] = None, priority: Optional[str] = None) -> str:
    """
    Update details of an existing task.
    
    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to update.
        title: Optional new title.
        description: Optional new description.
        due_date: Optional new due date.
        priority: Optional new priority.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return f"Task {task_id} not found."
        
        if title: task.title = title
        if description: task.description = description
        if due_date: task.due_date = due_date
        if priority:
            try:
                task.priority = TaskPriority(priority.lower())
            except ValueError:
                pass
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return f"Task {task_id} updated successfully."

@function_tool
@mcp.tool()
def delete_task(user_id: str, task_id: int) -> str:
    """
    Delete a task from the system.
    
    Args:
        user_id: The ID of the authenticated user.
        task_id: The ID of the task to delete.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return f"Task {task_id} not found."
        
        session.delete(task)
        session.commit()
        return f"Task {task_id} deleted."