import pytest
from src.services.task_service import TaskService
from src.models.task import TaskStatus

def test_add_task():
    service = TaskService()
    task = service.add_task("Buy milk")
    
    assert task.id == 1
    assert task.description == "Buy milk"
    assert task.status == TaskStatus.INCOMPLETE
    assert len(service._tasks) == 1

def test_add_task_increments_id():
    service = TaskService()
    t1 = service.add_task("Task 1")
    t2 = service.add_task("Task 2")
    
    assert t1.id == 1
    assert t2.id == 2

def test_list_tasks():
    service = TaskService()
    assert len(service.list_tasks()) == 0
    
    service.add_task("Task 1")
    service.add_task("Task 2")
    
    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].description == "Task 1"
    assert tasks[1].description == "Task 2"

def test_mark_complete():
    service = TaskService()
    task = service.add_task("Task 1")
    updated = service.mark_complete(task.id)
    assert updated.status == TaskStatus.COMPLETE

def test_mark_incomplete():
    service = TaskService()
    task = service.add_task("Task 1")
    service.mark_complete(task.id)
    updated = service.mark_incomplete(task.id)
    assert updated.status == TaskStatus.INCOMPLETE

def test_mark_complete_not_found_raises_error():
    service = TaskService()
    from src.lib.errors import TaskNotFoundError
    with pytest.raises(TaskNotFoundError):
        service.mark_complete(999)

def test_update_task():
    service = TaskService()
    task = service.add_task("Old desc")
    updated = service.update_task(task.id, "New desc")
    assert updated.description == "New desc"
    assert service.get_task(task.id).description == "New desc"

def test_update_task_not_found():
    service = TaskService()
    from src.lib.errors import TaskNotFoundError
    with pytest.raises(TaskNotFoundError):
        service.update_task(999, "desc")

def test_update_task_empty_desc():
    service = TaskService()
    task = service.add_task("Old desc")
    with pytest.raises(ValueError):
        service.update_task(task.id, "")

def test_delete_task():
    service = TaskService()
    task = service.add_task("To delete")
    service.delete_task(task.id)
    assert len(service.list_tasks()) == 0
    assert service.get_task(task.id) is None

def test_delete_task_not_found():
    service = TaskService()
    from src.lib.errors import TaskNotFoundError
    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)
