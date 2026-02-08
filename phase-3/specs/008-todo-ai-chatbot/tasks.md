# Tasks: Phase III Todo AI Chatbot

**Input**: Design documents from `/specs/008-todo-ai-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: US1, US2, US3
- **Paths**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (`api/`, `agents/`, `mcp/`, `models/`, `services/`) in `backend/src/`
- [x] T002 [P] Initialize Python environment and install `fastapi`, `openai-agents`, `mcp`, `sqlmodel`, `psycopg2-binary` in `backend/`
- [x] T003 [P] Configure environment variables template (`.env.example`) with `DATABASE_URL`, `OPENAI_API_KEY`, and `BETTER_AUTH_SECRET` in `backend/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and database setup

- [x] T004 Define SQLModel entities for `Task`, `Conversation`, and `Message` in `backend/src/models/`
- [x] T005 [P] Setup database engine and session management in `backend/src/services/db.py`
- [x] T006 [P] Implement authentication dependency using Better Auth in `backend/src/auth/`
- [x] T007 Initialize MCP server skeleton and tool registry in `backend/src/mcp/server.py`
- [x] T008 [P] Configure FastAPI app with CORS and base error handlers in `backend/src/main.py`

**Checkpoint**: Foundation ready - User stories can begin

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Allow users to add tasks via natural language.

**Independent Test**: Send "Add task buy milk" to chat and verify task appears in DB.

### Implementation for User Story 1

- [x] T009 [US1] Implement `add_task` MCP tool handler in `backend/src/mcp/tools.py`
- [x] T010 [US1] Define OpenAI Agent with `add_task` tool registration in `backend/src/agents/todo_agent.py`
- [x] T011 [US1] Implement `/api/{user_id}/chat` POST endpoint with basic message persistence in `backend/src/api/chat.py`
- [x] T012 [US1] Integrate OpenAI Agent into the chat endpoint to process messages and call tools in `backend/src/api/chat.py`
- [x] T013 [US1] Setup OpenAI ChatKit frontend integration in `frontend/src/app/chat/page.tsx`

**Checkpoint**: User Story 1 functional

---

## Phase 4: User Story 2 - Natural Language Task Management (Priority: P1)

**Goal**: CRUD tasks (list, update, complete, delete) via conversation.

**Independent Test**: Ask "What are my tasks?" and "Complete task 1" and verify updates.

### Implementation for User Story 2

- [x] T014 [P] [US2] Implement `list_tasks` and `complete_task` MCP tool handlers in `backend/src/mcp/tools.py`
- [x] T015 [P] [US2] Implement `update_task` and `delete_task` MCP tool handlers in `backend/src/mcp/tools.py`
- [x] T016 [US2] Update OpenAI Agent system prompt with management behavior rules in `backend/src/agents/todo_agent.py`
- [x] T017 [US2] Refine chat endpoint to handle complex tool invocation results in `backend/src/api/chat.py`

**Checkpoint**: User Story 2 functional

---

## Phase 5: User Story 3 - Persistent Conversation History (Priority: P2)

**Goal**: Contextual continuity across restarts.

**Independent Test**: Send a message, restart server, and verify agent remembers context.

### Implementation for User Story 3

- [x] T018 [US3] Implement logic to retrieve full conversation history from `Message` table in `backend/src/api/chat.py`
- [x] T019 [US3] Ensure `conversation_id` is correctly passed and handled by the frontend ChatKit in `frontend/src/app/chat/page.tsx`
- [x] T020 [US3] Verify stateless reconstruction of agent session from DB history on every request in `backend/src/api/chat.py`

**Checkpoint**: All user stories functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final audit and security checks

- [x] T021 [P] Implement detailed tool call logging for auditability in `backend/src/services/logger.py`
- [x] T022 Security review: Verify strict `user_id` scoping in all SQL queries in `backend/src/`
- [x] T023 Run end-to-end validation against `quickstart.md`
- [x] T024 Final documentation update: API and MCP tool descriptions in `specs/008-todo-ai-chatbot/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### Parallel Opportunities

- T002 and T003 in Setup
- T005, T006, and T008 in Foundational
- T014 and T015 in User Story 2
- T021 in Polish

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently using the criteria "Add task buy milk".

### Incremental Delivery

1. Add User Story 2 (Task Management)
2. Add User Story 3 (Contextual Persistence)
3. Each story adds value without breaking previous stories.