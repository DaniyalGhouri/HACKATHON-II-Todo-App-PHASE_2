from datetime import datetime
from typing import Optional, Annotated, Any
from sqlmodel import Session, select
from ..models.task import Task, TaskPriority
from ..services.db import engine
from ..services.logger import log_tool_call
from .server import mcp
from agents import function_tool

@function_tool
@mcp.tool()
def add_task(
    user_id: Annotated[str, "The ID of the authenticated user"], 
    title: Annotated[str, "The title of the task"], 
    description: Annotated[Optional[str], "Optional detailed description"] = None, 
    due_date: Annotated[Optional[datetime], "Optional due date/time"] = None, 
    priority: Annotated[str, "Task priority (low, medium, high). Defaults to medium"] = "medium"
) -> str:
    """
    Create a new todo task.
    """
    try:
        p_enum = TaskPriority(priority.lower())
    except Exception:
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
def list_tasks(
    user_id: Annotated[str, "The ID of the authenticated user"], 
    status_filter: Annotated[str, "Filter by status: 'all', 'completed', or 'pending'."] = "all"
) -> str:
    """
    List user tasks with an optional filter.
    """
    completed_val = None
    if status_filter == "completed":
        completed_val = True
    elif status_filter == "pending":
        completed_val = False

    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if completed_val is not None:
            statement = statement.where(Task.is_completed == completed_val)
        
        tasks = session.exec(statement).all()
        if not tasks:
            return "No tasks found."
        
        output = f"Your tasks ({status_filter}):\n"
        for t in tasks:
            status = "[x]" if t.is_completed else "[ ]"
            due = f", Due: {t.due_date.strftime('%Y-%m-%d %H:%M')}" if t.due_date else ""
            output += f"ID {t.id}: {status} {t.title} (Priority: {t.priority.value}{due})\n"
        return output

@function_tool
@mcp.tool()
def update_task(
    user_id: Annotated[str, "The ID of the authenticated user"], 
    task_id: Annotated[int, "The integer ID of the task to update"], 
    title: Annotated[Optional[str], "New title"] = None, 
    description: Annotated[Optional[str], "New description"] = None, 
    due_date: Annotated[Optional[datetime], "New due date"] = None, 
    priority: Annotated[Optional[str], "New priority (low, medium, high)"] = None
) -> str:
    """
    Update an existing task.
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return f"Task {task_id} not found. Use list_tasks to find the correct ID."
        
        if title: task.title = title
        if description: task.description = description
        if due_date: task.due_date = due_date
        if priority:
            try:
                task.priority = TaskPriority(priority.lower())
            except Exception:
                pass
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        return f"Task {task_id} updated successfully."

@function_tool
@mcp.tool()
def complete_task(
    user_id: Annotated[str, "The ID of the authenticated user"], 
    task_id: Annotated[int, "The integer ID of the task to complete"]
) -> str:
    """Mark a task as finished."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task: return f"Task {task_id} not found."
        task.is_completed = True
        session.add(task)
        session.commit()
        return f"Task {task_id} completed."

@function_tool
@mcp.tool()
def delete_task(
    user_id: Annotated[str, "The ID of the authenticated user"], 
    task_id: Annotated[int, "The integer ID of the task to delete"]
) -> str:
    """Delete a task."""
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task: return f"Task {task_id} not found."
        session.delete(task)
        session.commit()
        return f"Task {task_id} deleted."
