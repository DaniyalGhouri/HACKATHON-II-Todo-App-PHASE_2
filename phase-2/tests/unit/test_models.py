import pytest
from src.models.task import Task, TaskStatus

def test_task_creation():
    task = Task(id=1, description="Buy milk")
    assert task.id == 1
    assert task.description == "Buy milk"
    assert task.status == TaskStatus.INCOMPLETE

def test_task_empty_description_raises_error():
    with pytest.raises(ValueError):
        Task(id=1, description="")
    with pytest.raises(ValueError):
        Task(id=1, description="   ")
