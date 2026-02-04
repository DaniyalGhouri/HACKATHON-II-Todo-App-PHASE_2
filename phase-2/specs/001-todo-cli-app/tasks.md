---
description: "Task list template for feature implementation"
---

# Tasks: Todo In-Memory Python Console Application

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), data-model.md, contracts/cli-commands.md

**Tests**: Tests are included as per "Test-First Rigor" in Constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directories (src, tests) per implementation plan
- [x] T002 Initialize Python project (pyproject.toml/requirements.txt) with pytest dependency
- [x] T003 [P] Configure pytest in pyproject.toml
- [x] T004 Create empty __init__.py files in src/models, src/services, src/cli, tests/unit, tests/integration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Task entity (dataclass) in src/models/task.py
- [x] T006 [P] Create TaskService class shell in src/services/task_service.py
- [x] T007 [P] Create CLI main entry point in src/cli/main.py with basic argument parsing shell
- [x] T008 [P] Implement basic error handling utils in src/lib/errors.py (if needed, else inline)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add a Task (Priority: P1) 🎯 MVP

**Goal**: Users can add a new task with a description.

**Independent Test**: `python -m src.cli.main add "Buy milk"` -> Output: "Task added. ID: 1"

### Tests for User Story 1

- [x] T009 [P] [US1] Create unit test for Task creation in tests/unit/test_models.py
- [x] T010 [P] [US1] Create unit test for TaskService.add_task in tests/unit/test_service.py
- [x] T011 [P] [US1] Create integration test for 'add' command in tests/integration/test_cli.py

### Implementation for User Story 1

- [x] T012 [US1] Implement Task model validation (non-empty description) in src/models/task.py
- [x] T013 [US1] Implement TaskService.add_task method (ID generation, storage) in src/services/task_service.py
- [x] T014 [US1] Implement 'add' command handler in src/cli/commands.py
- [x] T015 [US1] Wire 'add' command in src/cli/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see a list of all tasks.

**Independent Test**: `python -m src.cli.main list` -> Output list of tasks or "No tasks found".

### Tests for User Story 2

- [x] T016 [P] [US2] Create unit test for TaskService.list_tasks in tests/unit/test_service.py
- [x] T017 [P] [US2] Create integration test for 'list' command in tests/integration/test_cli.py

### Implementation for User Story 2

- [x] T018 [US2] Implement TaskService.list_tasks method in src/services/task_service.py
- [x] T019 [US2] Implement 'list' command handler (formatting) in src/cli/commands.py
- [x] T020 [US2] Wire 'list' command in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task status.

**Independent Test**: `python -m src.cli.main complete 1` -> Output: "Task 1 marked complete."

### Tests for User Story 3

- [x] T021 [P] [US3] Create unit tests for TaskService.mark_complete/incomplete in tests/unit/test_service.py
- [x] T022 [P] [US3] Create integration tests for 'complete'/'incomplete' commands in tests/integration/test_cli.py

### Implementation for User Story 3

- [x] T023 [US3] Implement TaskService methods for status toggling in src/services/task_service.py
- [x] T024 [US3] Implement 'complete' and 'incomplete' command handlers in src/cli/commands.py
- [x] T025 [US3] Wire status commands in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Update Task Description (Priority: P3)

**Goal**: Users can modify task description.

**Independent Test**: `python -m src.cli.main update 1 "New desc"` -> Output: "Task 1 updated."

### Tests for User Story 4

- [x] T026 [P] [US4] Create unit test for TaskService.update_task in tests/unit/test_service.py
- [x] T027 [P] [US4] Create integration test for 'update' command in tests/integration/test_cli.py

### Implementation for User Story 4

- [x] T028 [US4] Implement TaskService.update_task method in src/services/task_service.py
- [x] T029 [US4] Implement 'update' command handler in src/cli/commands.py
- [x] T030 [US4] Wire 'update' command in src/cli/main.py

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can remove tasks.

**Independent Test**: `python -m src.cli.main delete 1` -> Output: "Task 1 deleted."

### Tests for User Story 5

- [x] T031 [P] [US5] Create unit test for TaskService.delete_task in tests/unit/test_service.py
- [x] T032 [P] [US5] Create integration test for 'delete' command in tests/integration/test_cli.py

### Implementation for User Story 5

- [x] T033 [US5] Implement TaskService.delete_task method in src/services/task_service.py
- [x] T034 [US5] Implement 'delete' command handler in src/cli/commands.py
- [x] T035 [US5] Wire 'delete' command in src/cli/main.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 Update quickstart.md with actual usage examples if changed
- [x] T037 Ensure strict type checking (mypy) passes across src/
- [x] T038 Verify all tests pass
- [x] T039 Clean up any temporary files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup
- **User Stories (Phase 3+)**: All depend on Foundational phase
- **Polish (Phase 8)**: Depends on all user stories

### User Story Dependencies

- **US1 (Add)**: Independent (MVP)
- **US2 (View)**: Independent logic, but testing relies on Add logic (or mocking)
- **US3 (Status)**: Needs Tasks to exist (US1 logic)
- **US4 (Update)**: Needs Tasks to exist (US1 logic)
- **US5 (Delete)**: Needs Tasks to exist (US1 logic)

### Parallel Opportunities

- All [P] tasks within a phase can run in parallel.
- Once Phase 2 is done, US1 and US2 can theoretically start in parallel if mocked correctly, but linear US1 -> US2 is safer for this scale.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2
2. Complete Phase 3 (Add Task)
3. Validate: Can add tasks? (Check via debugger or internal logs if List not ready)

### Incremental Delivery

1. Foundation -> Add Task (US1) -> View Tasks (US2) -> MVP Complete.
2. Add Status (US3) -> Release 0.2.
3. Add Update/Delete (US4/5) -> Release 1.0.