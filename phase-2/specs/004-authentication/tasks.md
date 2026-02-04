---
description: "Task list for Authentication Feature"
---

# Tasks: Authentication

**Input**: Design documents from `/specs/004-authentication/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create auth feature directory structure `backend/src/auth` `frontend/src/app/(auth)` `frontend/src/lib`
- [x] T002 [P] Install `better-auth` in frontend: `cd frontend && npm install better-auth`
- [x] T003 [P] Install `pyjwt` in backend: `cd backend && pip install pyjwt`
- [x] T004 [P] Update `.env` templates with `BETTER_AUTH_SECRET` and `BETTER_AUTH_URL`

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create backend JWT verification utility in `backend/src/auth/utils.py`
- [ ] T006 Implement `get_current_user` dependency in `backend/src/auth/dependencies.py`
- [ ] T007 Configure Better Auth client in `frontend/src/lib/auth.ts`
- [x] T008 Implement Backend Auth Middleware (if needed globally) in `backend/src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

## Phase 3: User Story 1 - User Signup & Login (Priority: P1) 🎯 MVP

**Goal**: User can sign up and log in via frontend, receiving a session.

**Independent Test**: Frontend Login Page -> Submit -> Redirect to Dashboard -> Cookie/Token present.

### Implementation for User Story 1

- [x] T009 [US1] Create Login Page UI in `frontend/src/app/(auth)/login/page.tsx`
- [x] T010 [US1] Create Signup Page UI in `frontend/src/app/(auth)/signup/page.tsx`
- [x] T011 [US1] Implement Auth Form Component in `frontend/src/components/auth-form.tsx`
- [x] T012 [US1] Configure Better Auth API route in `frontend/src/app/api/auth/[...all]/route.ts`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

## Phase 4: User Story 2 - Authenticated API Access (Priority: P1)

**Goal**: Frontend attaches JWT to API requests; Backend verifies it.

**Independent Test**: Fetch to protected API returns 200 with token, 401 without.

### Implementation for User Story 2

- [x] T013 [US2] Create API Client wrapper with Auth Header in `frontend/src/lib/api-client.ts`
- [x] T014 [US2] Update Backend `main.py` to protect example route with `get_current_user` dependency
- [x] T015 [US2] Add manual test script for token verification in `backend/tests/manual_auth_check.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

## Phase 5: User Story 3 - Session Persistence (Priority: P2)

**Goal**: User remains logged in across refreshes.

**Independent Test**: Refresh page -> User still logged in.

### Implementation for User Story 3

- [x] T016 [US3] Implement Session Provider/Hook in `frontend/src/components/session-provider.tsx`
- [x] T017 [US3] Add layout wrapper to check session state in `frontend/src/app/layout.tsx`

**Checkpoint**: All user stories should now be independently functional

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T018 Run `quickstart.md` validation steps for Auth flow
- [x] T019 Ensure error messages on Login/Signup are user-friendly
- [x] T020 Security Audit: Verify `BETTER_AUTH_SECRET` is not exposed in public bundles

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Stories (Phase 3-5)**: Depend on Phase 2.

### User Story Dependencies

- **US1 (Login)**: Independent.
- **US2 (API Access)**: Depends on US1 (need token to test).
- **US3 (Persistence)**: Depends on US1.

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Setup & Foundation.
2. Implement Frontend Login (US1).
3. Implement Backend Verification (Foundation).
4. Implement API Client (US2).
5. Verify end-to-end flow.
