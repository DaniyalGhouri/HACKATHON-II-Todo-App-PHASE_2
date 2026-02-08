from typing import Generator
import os
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

# Import models to register them
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Fallback to sqlite for dev if not set (or raise error)
    DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
