from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import computed_field

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskPriority = TaskPriority.MEDIUM

class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    @computed_field
    @property
    def completed(self) -> bool:
        return self.is_completed

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None
    completed: Optional[bool] = None # For frontend compatibility