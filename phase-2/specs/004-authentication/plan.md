# Implementation Plan: Authentication

**Branch**: `004-authentication` | **Date**: 2026-01-19 | **Spec**: [specs/004-authentication/spec.md](../spec.md)
**Input**: Feature specification from `specs/004-authentication/spec.md`

## Summary

Implement secure authentication using Better Auth on the Frontend (Next.js) for handling Signup/Login and session management. The Backend (FastAPI) will independently verify JWTs issued by the frontend using a shared secret to protect API endpoints.

## Technical Context

**Language/Version**: Python 3.13 (Backend), TypeScript/Node (Frontend)
**Primary Dependencies**: 
- Frontend: `better-auth`, `next`, `react`
- Backend: `pyjwt`, `fastapi`
**Storage**: Neon PostgreSQL (Users table managed by Better Auth)
**Testing**: `pytest` (Backend), `jest`/`playwright` (Frontend - optional/future)
**Target Platform**: Web (Next.js App Router + FastAPI)
**Project Type**: Full-stack Web Application
**Security**: JWT (HS256) signed with shared secret.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven**: Derived from `specs/004-authentication/spec.md`.
- [x] **Full-Stack Web**: Separated Next.js and FastAPI.
- [x] **Modern Data Layer**: Uses Neon PostgreSQL.
- [x] **Authentication**: Uses Better Auth (Frontend) + JWT Verification (Backend).
- [x] **Agent-Exclusive**: Planning for agentic implementation.
- [x] **Test-First**: Plan includes testing strategy.

## Project Structure

### Documentation (this feature)

```text
specs/004-authentication/
├── plan.md              # This file
├── research.md          # Technical decisions
├── data-model.md        # User entity definition
├── quickstart.md        # How to run auth
├── contracts/           # API contracts (if any specific auth endpoints on backend)
└── tasks.md             # Implementation tasks
```

### Source Code

```text
backend/
├── src/
│   ├── auth/           # New module for JWT verification
│   │   ├── dependencies.py # FastAPI dependencies (get_current_user)
│   │   └── utils.py    # Token verification logic
│   └── main.py         # Update to include auth middleware/exception handlers
└── tests/
    └── unit/
        └── test_auth.py # Test JWT verification logic

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/     # Route group for auth pages
│   │   │   ├── login/
│   │   │   └── signup/
│   │   └── layout.tsx
│   ├── lib/
│   │   └── auth.ts     # Better Auth client configuration
│   └── components/
│       └── auth-form.tsx
```

**Structure Decision**: Standard "Separation of Concerns" structure. Frontend handles UI/Session; Backend handles stateless verification.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Independent Auth Verification | Security requirement | Using a shared session store (Redis) adds infrastructure complexity; Stateless JWT is simpler for Phase II. |
