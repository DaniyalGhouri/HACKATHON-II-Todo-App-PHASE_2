from src.services.task_service import TaskService
from src.lib.errors import TaskNotFoundError
import sys

class CommandHandler:
    def __init__(self):
        self.service = TaskService()

    def handle_add(self, description: str):
        try:
            task = self.service.add_task(description)
            print(f"Task added. ID: {task.id}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)

    def handle_list(self):
        tasks = self.service.list_tasks()
        if not tasks:
            print("No tasks found.")
            return

        print(f"{'ID':<4} {'Status':<12} {'Description'}")
        for task in tasks:
            status = "[x]" if task.status.value == "Complete" else "[ ]"
            print(f"{task.id:<4} {status:<12} {task.description}")

    def handle_update(self, task_id: int, description: str):
        try:
            self.service.update_task(task_id, description)
            print(f"Task {task_id} updated.")
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)

    def handle_delete(self, task_id: int):
        try:
            self.service.delete_task(task_id)
            print(f"Task {task_id} deleted.")
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)

    def handle_complete(self, task_id: int):
        try:
            self.service.mark_complete(task_id)
            print(f"Task {task_id} marked complete.")
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)

    def handle_incomplete(self, task_id: int):
        try:
            self.service.mark_incomplete(task_id)
            print(f"Task {task_id} marked incomplete.")
        except TaskNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
