# Research: Task CRUD Operations

## Unknowns & Clarifications

### 1. Database Model for Tasks
- **Context**: Need to persist tasks with user isolation.
- **Decision**: Use SQLModel (SQLAlchemy wrapper).
- **Rationale**: Project standard for Phase II. Simplifies Pydantic integration.
- **Alternatives**: Raw SQLAlchemy (more verbose), Tortoise ORM (async native but less Pydantic integration).

### 2. User Identification in Backend
- **Context**: Need to identify `user_id` from JWT.
- **Decision**: Implement a middleware or dependency `get_current_user` that decodes JWT using `PyJWT`.
- **Rationale**: Standard, secure, and complies with Constitution (Backend verifies independently).

### 3. API Structure
- **Context**: REST endpoints for CRUD.
- **Decision**: Use FastAPI `APIRouter` with prefix `/api/tasks`.
- **Note**: The spec mentioned `/api/{user_id}/tasks` in "REST API Endpoints" feature, but strictly speaking, `user_id` in URL is redundant if we have the token. However, the Overview Spec and API Spec mandated it.
- **Clarification**: I will follow the strict `spec.md` for *this* feature (`003-task-crud`) which focuses on the logic. The URL structure was defined in `005-rest-api-endpoints`. I will align with `005`'s URL pattern `/api/{user_id}/tasks` to ensure consistency.

## Technology Decisions

| Technology | Choice | Reasoning |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | Async, Pydantic support, automatic OpenAPI docs. |
| **ORM** | SQLModel | Hybrid Pydantic/SQLAlchemy models, great for FastAPI. |
| **Database** | Neon (Postgres) | Serverless, mandated by Constitution. |
| **Auth Verification** | PyJWT | Standard library for JWT decoding/verification. |

## Patterns

- **Repository Pattern**: Encapsulate DB logic for Tasks in `TaskService` or `TaskRepository` to separate from API routes.
- **Dependency Injection**: Inject DB session and User context into route handlers.
