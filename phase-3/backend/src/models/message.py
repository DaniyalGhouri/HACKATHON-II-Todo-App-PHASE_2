from datetime import datetime
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id", index=True)
    role: str  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
