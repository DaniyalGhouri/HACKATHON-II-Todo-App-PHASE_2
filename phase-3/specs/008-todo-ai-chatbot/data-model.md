# Data Model: Phase III Todo AI Chatbot

## Entities

### 1. Task
Represents a todo item managed by the user.

| Field | Type | Description |
|-------|------|-------------|
| id | int (PK) | Unique identifier |
| title | str | Task title |
| description | str (opt) | Detailed task description |
| due_date | datetime (opt) | When the task is due |
| is_completed | bool | Completion status |
| user_id | str | Owner of the task (authenticated user) |
| created_at | datetime | Timestamp of creation |
| updated_at | datetime | Timestamp of last update |

### 2. Conversation
Represents a chat session between a user and the assistant.

| Field | Type | Description |
|-------|------|-------------|
| id | uuid (PK) | Unique identifier |
| user_id | str | The user involved in the conversation |
| created_at | datetime | When the conversation started |

### 3. Message
An individual exchange in a conversation.

| Field | Type | Description |
|-------|------|-------------|
| id | int (PK) | Unique identifier |
| conversation_id | uuid (FK) | Reference to Conversation |
| role | str | 'user' or 'assistant' |
| content | str | The message text |
| created_at | datetime | When the message was sent |

## Relationships
- **Conversation** (1) -> (N) **Message**
- **User** (implicitly via `user_id`) -> (N) **Task**
- **User** (implicitly via `user_id`) -> (N) **Conversation**

## Constraints
- Every record MUST have a `user_id`.
- Data access MUST always filter by `user_id`.
