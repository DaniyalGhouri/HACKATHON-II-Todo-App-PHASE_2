from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import UniqueConstraint, Table

class TaskBase(SQLModel):
    title: str = Field(index=True, min_length=1, max_length=200, regex=r"^[ -~]*$") # FR-004: Task Title constraints
    description: Optional[str] = Field(default=None, max_length=1000) # FR-005: Max length for description
    completed: bool = Field(default=False) # Renamed from is_completed

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True) # FR-002: Associate with user ID
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "title", name="uq_user_id_title"),) # FR-008: Unique per user

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, regex=r"^[ -~]*$")
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
