from typing import List, Optional, Dict
from src.models.task import Task, TaskStatus
from src.lib.errors import TaskNotFoundError

class TaskService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _get_task_or_raise(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task ID {task_id} not found")
        return self._tasks[task_id]

    def add_task(self, description: str) -> Task:
        task = Task(id=self._next_id, description=description)
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, description: str) -> Task:
        task = self._get_task_or_raise(task_id)
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        task.description = description
        return task

    def delete_task(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task ID {task_id} not found")
        del self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        task = self._get_task_or_raise(task_id)
        task.status = TaskStatus.COMPLETE
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        task = self._get_task_or_raise(task_id)
        task.status = TaskStatus.INCOMPLETE
        return task
