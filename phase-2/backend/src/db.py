from sqlmodel import create_engine, Session, SQLModel
import os
# Import your models here to ensure they are registered with SQLModel.metadata
from src.models.task import Task # Changed to absolute import
# from src.models.user import User # Uncomment if User model is defined as table=True

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
