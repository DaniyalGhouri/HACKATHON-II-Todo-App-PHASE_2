from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(Enum):
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.INCOMPLETE
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
