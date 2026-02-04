# Feature Specification: Task CRUD Operations

**Feature Branch**: `003-task-crud`
**Created**: 2026-01-19
**Status**: Draft
**Input**: User description: "Create a detailed feature specification for Task CRUD operations..."

## User Scenarios & Testing

### User Story 1 - Create Task (Priority: P1)

As an authenticated user, I want to create a new task with a title and optional description so that I can track what I need to do.

**Why this priority**: Essential for adding data to the system; without this, the app is empty.

**Independent Test**:
- Log in as User A.
- Send POST /tasks with title "Buy Milk".
- Verify response 201 Created.
- Send GET /tasks and verify "Buy Milk" is in the list.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they submit a valid task (title present, within length/char limits), **Then** the task is saved and associated with their User ID.
2. **Given** an authenticated user, **When** they submit a task without a title, **Then** the system returns 422 Validation Error.
3. **Given** an authenticated user, **When** they submit a task with a title exceeding 200 characters or containing unprintable characters, **Then** the system returns 422 Validation Error.
4. **Given** an authenticated user, **When** they submit a task with a title that already exists for them, **Then** the system returns 409 Conflict.
5. **Given** an unauthenticated user, **When** they try to create a task, **Then** the system returns 401 Unauthorized.

---

### User Story 2 - View My Tasks (Priority: P1)

As an authenticated user, I want to view a list of only my tasks so that I can see my workload without seeing others' private data.

**Why this priority**: Validates data persistence and privacy/isolation rules.

**Independent Test**:
- User A creates "Task A".
- User B creates "Task B".
- User A requests GET /tasks.
- Verify response contains ONLY "Task A".

**Acceptance Scenarios**:

1. **Given** multiple users with tasks, **When** a user requests their task list, **Then** they see only tasks where `user_id` matches their own.
2. **Given** a user with no tasks, **When** they request their task list, **Then** they receive an empty list (not an error).

---

### User Story 3 - Update Task Status (Priority: P2)

As an authenticated user, I want to toggle a task's completion status so that I can mark work as done.

**Why this priority**: Core workflow functionality (Do -> Done).

**Independent Test**:
- Create task (default status: incomplete).
- Send PATCH /tasks/{id} with `is_completed=true`.
- Verify response shows updated status.
- Fetch task again to verify persistence.

**Acceptance Scenarios**:

1. **Given** an existing task owned by the user, **When** they update its status, **Then** the change is saved.
2. **Given** an existing task owned by the user, **When** they attempt to update the task with a null or empty title, **Then** the system returns 400 Bad Request.
3. **Given** an existing task owned by the user, **When** they update the task with a title that already exists for them (another task), **Then** the system returns 409 Conflict.
4. **Given** a task owned by User A, **When** User B tries to update it, **Then** the system returns 404 Not Found (to prevent ID enumeration) or 403 Forbidden.

---

### User Story 4 - Delete Task (Priority: P3)

As an authenticated user, I want to permanently remove a task so that I can declutter my list.

**Why this priority**: Clean up functionality.

**Independent Test**:
- Create task.
- Send DELETE /tasks/{id}.
- Verify response 204 No Content.
- Send GET /tasks/{id} and verify 404 Not Found.

**Acceptance Scenarios**:

1. **Given** an existing task owned by the user, **When** they request deletion, **Then** it is permanently removed.
2. **Given** a task owned by User A, **When** User B tries to delete it, **Then** the operation fails (404/403).

## Requirements

### Functional Requirements

- **FR-001**: System MUST require authentication for all Task operations.
- **FR-002**: System MUST associate every created task with the authenticated user's ID (derived from JWT).
- **FR-003**: System MUST enforce strict data isolation (Users can never access/modify others' tasks).
- **FR-004**: Task Title is MANDATORY, MUST have a minimum length of 1 character, a maximum length of 200 characters, and contain only printable ASCII characters.
- **FR-005**: Task Description is OPTIONAL, and MUST have a maximum length of 1000 characters.
- **FR-006**: Task Completion Status MUST default to `false` (incomplete) upon creation.
- **FR-007**: System MUST return 404 Not Found if a user attempts to access a task ID that belongs to another user (Security: Prevent ID scanning).
- **FR-008**: Task titles MUST be unique per user (a user cannot have two tasks with the exact same title). Two different users may have tasks with the same title.
- **FR-009**: When updating a task, an attempt to set the title to null or an empty string MUST result in a 400 Bad Request error.

### Key Entities

- **Task**:
    - `id`: Unique Identifier (UUID or Int).
    - `user_id`: Foreign Key to User (Authentication Source).
    - `title`: String (Required, Min 1, Max 200, Unique per user).
    - `description`: String (Optional, Max 1000).
    - `is_completed`: Boolean (Default: False).
    - `created_at`: Timestamp.
    - `updated_at`: Timestamp.

## Success Criteria

### Measurable Outcomes

- **SC-001**: User can create a task and retrieve it within 500ms.
- **SC-002**: 100% of CRUD operations on another user's Task ID result in rejection (404/403).
- **SC-003**: Task persistence is verified across backend restarts.
- **SC-004**: API adheres to standard HTTP status codes (200, 201, 204, 400, 401, 403, 404, 409, 422).

## Assumptions & Constraints

- **Constraints**: 
    - No bulk operations in this phase.
    - No "Archived" state (Delete is permanent).
- **Assumptions**:
    - Frontend handles date formatting.
    - User ID is available in `request.state.user` or similar middleware object after JWT verification.

## Edge Cases

- **EC-001**: Tasks with very long titles (e.g., exactly 200 chars) or descriptions (e.g., exactly 1000 chars) MUST be handled gracefully (stored and displayed without truncation by backend). Frontend display may truncate for UI purposes but data integrity is maintained.
- **EC-002**: Attempting to create a task with a title that already exists for the current user MUST result in a 409 Conflict error.
- **EC-003**: Attempting to update a task's title to one that already exists for the current user (another task) MUST result in a 409 Conflict error.

## Out of Scope

- Task Sharing / Collaboration (to focus on core multi-user isolation).
- Task Due Dates / Reminders (to keep MVP focused on basic task management).
- Task Categories / Tags (to keep MVP focused on basic task management).
- Bulk Delete / Bulk Update (to keep MVP focused on single-item operations).