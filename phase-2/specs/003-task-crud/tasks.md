---
description: "Task list for Task CRUD Operations"
---

# Tasks: Task CRUD Operations

**Input**: Design documents from `/specs/003-task-crud/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create feature directory structure `backend/src/api` `backend/src/models` `backend/src/services`
- [x] T002 [P] Install dependencies `fastapi` `sqlmodel` `pyjwt` in `backend/requirements.txt`
- [x] T003 [P] Configure SQLModel database connection in `backend/src/db.py`

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create base `User` context dependency in `backend/src/auth/dependencies.py`
- [x] T005 Create `Task` SQLModel entity in `backend/src/models/task.py`
- [x] T006 Implement database migration/initialization for `Task` table in `backend/src/db.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

## Phase 3: User Story 1 - Create Task (Priority: P1) 🎯 MVP

**Goal**: Authenticated user can create a new task with a title.

**Independent Test**: POST /api/{user_id}/tasks with title returns 201 Created and task object.

### Implementation for User Story 1

- [x] T007 [US1] Implement `create_task` logic in `backend/src/services/task_service.py`
- [x] T008 [US1] Create POST endpoint `/api/{user_id}/tasks` in `backend/src/api/tasks.py`
- [x] T009 [US1] Register task router in `backend/src/main.py`
- [x] T010 [US1] Add manual test script for creation in `backend/tests/manual_create_task.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

## Phase 4: User Story 2 - View My Tasks (Priority: P1)

**Goal**: Authenticated user can view only their own tasks.

**Independent Test**: GET /api/{user_id}/tasks returns list of tasks for that user only.

### Implementation for User Story 2

- [x] T011 [US2] Implement `get_user_tasks` logic in `backend/src/services/task_service.py`
- [x] T012 [US2] Create GET endpoint `/api/{user_id}/tasks` in `backend/src/api/tasks.py`
- [x] T013 [US2] Add manual test script for listing tasks in `backend/tests/manual_list_tasks.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

## Phase 5: User Story 3 - Update Task Status (Priority: P2)

**Goal**: Authenticated user can toggle task completion status.

**Independent Test**: PATCH /api/{user_id}/tasks/{id} updates status and persists.

### Implementation for User Story 3

- [x] T014 [US3] Implement `update_task` logic with ownership check in `backend/src/services/task_service.py`
- [x] T015 [US3] Create PATCH endpoint `/api/{user_id}/tasks/{id}` in `backend/src/api/tasks.py`
- [x] T016 [US3] Add manual test script for updating task in `backend/tests/manual_update_task.py`

**Checkpoint**: All user stories should now be independently functional

## Phase 6: User Story 4 - Delete Task (Priority: P3)

**Goal**: Authenticated user can permanently delete a task.

**Independent Test**: DELETE /api/{user_id}/tasks/{id} removes task; subsequent GET returns 404.

### Implementation for User Story 4

- [x] T017 [US4] Implement `delete_task` logic with ownership check in `backend/src/services/task_service.py`
- [x] T018 [US4] Create DELETE endpoint `/api/{user_id}/tasks/{id}` in `backend/src/api/tasks.py`
- [x] T019 [US4] Add manual test script for deletion in `backend/tests/manual_delete_task.py`

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T020 Run `quickstart.md` validation steps
- [x] T021 Ensure all API endpoints handle 404/403 errors correctly per spec

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Stories (Phase 3-6)**: Depend on Phase 2. Can run sequentially or in parallel.

### User Story Dependencies

- **US1 (Create)**: Independent.
- **US2 (View)**: Independent (but needs data from US1 to be interesting).
- **US3 (Update)**: Independent (needs data).
- **US4 (Delete)**: Independent (needs data).

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Setup & Foundation.
2. Implement Creation (US1).
3. Implement Listing (US2).
4. Verify MVP flow (Create -> List).

### Incremental Delivery

1. Add Update (US3).
2. Add Delete (US4).
