# Data Model: Todo In-Memory Python Console Application

**Feature Branch**: `001-todo-cli-app`

## Entities

### Task

Represents a single item of work.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| id | int | Yes | Auto-inc | Unique identifier (1, 2, 3...) |
| description | str | Yes | - | Content of the task. Non-empty. |
| status | Enum | Yes | Incomplete | Current state (`Incomplete` or `Complete`) |
| created_at | datetime | No | Now | Creation timestamp (implicit/internal use) |

#### Validation Rules
1. `description` must not be empty or whitespace only.
2. `id` must be a positive integer.

## Storage Schema (In-Memory)

The application state is held in a singleton or service class instance during runtime.

```python
class TaskRepository:
    _tasks: Dict[int, Task] = {}
    _next_id: int = 1
```

- **Persistence**: None (Ephemeral).
- **Concurrency**: Not applicable (Single threaded CLI).
