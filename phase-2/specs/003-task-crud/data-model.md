# Data Model: Task

## Entity: Task

Represents a single item of work to be tracked by a user.

### Attributes

| Field | Type | Required | Description | Constraints |
| :--- | :--- | :--- | :--- | :--- |
| `id` | UUID | Yes | Unique Identifier | Primary Key, Auto-generated |
| `user_id` | String | Yes | Owner Identifier | Foreign Key (Virtual), Indexed |
| `title` | String | Yes | Task summary | Max length 255 |
| `description` | String | No | Detailed info | Nullable |
| `is_completed` | Boolean | Yes | Status | Default `False` |
| `created_at` | DateTime | Yes | Creation timestamp | Default `Now()` |
| `updated_at` | DateTime | Yes | Last update | Default `Now()`, OnUpdate `Now()` |

### Relationships

- **User**: Many-to-One (Implicit via `user_id`). A Task belongs to exactly one User.

### SQLModel Definition (Draft)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class TaskBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)

class Task(TaskBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
```
