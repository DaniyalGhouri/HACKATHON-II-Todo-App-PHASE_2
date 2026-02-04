# Feature Specification: REST API Endpoints

**Feature Branch**: `005-rest-api-endpoints`
**Created**: 2026-01-19
**Status**: Draft
**Input**: User description: "Define the REST API contract for Phase II. This specification defines endpoints only..."

## User Scenarios & Testing

### User Story 1 - Standardized API Access (Priority: P1)

As a frontend developer, I want a consistent, RESTful API contract so that I can implement the UI without ambiguity.

**Why this priority**: Defines the contract between Frontend and Backend.

**Independent Test**:
- Send requests to all defined endpoints using `curl` or Postman.
- Verify status codes and JSON structure match the spec.

**Acceptance Scenarios**:

1. **Given** a valid GET request to `/api/{user_id}/tasks`, **When** sent with a valid JWT, **Then** return 200 OK with a list of tasks.
2. **Given** a POST request to `/api/{user_id}/tasks`, **When** sent with valid JSON, **Then** return 201 Created with the new task.

---

### User Story 2 - Security Enforcement (Priority: P0)

As a system administrator, I want to ensure that API endpoints strictly enforce user isolation so that data breaches are impossible via the API.

**Why this priority**: Security critical.

**Independent Test**:
- Authenticate as User A (ID: 1).
- Try to GET `/api/2/tasks` (User B's tasks).
- Verify 403 Forbidden response.

**Acceptance Scenarios**:

1. **Given** an authenticated user (ID X), **When** requesting `/api/Y/tasks` where X != Y, **Then** the system returns 403 Forbidden.
2. **Given** an unauthenticated request, **When** accessing any endpoint, **Then** return 401 Unauthorized.

## Requirements

### Functional Requirements

- **FR-001**: System MUST expose a RESTful API with JSON content negotiation.
- **FR-002**: All endpoints MUST require a valid JWT in the `Authorization` header.
- **FR-003**: System MUST enforce URL-based ownership checks (User ID in URL must match Token ID).

### API Contract

#### 1. List Tasks
- **GET** `/api/{user_id}/tasks`
- **Response**: 200 OK `[Task]`

#### 2. Create Task
- **POST** `/api/{user_id}/tasks`
- **Body**: `{"title": "string", "description": "string"}`
- **Response**: 201 Created `Task`

#### 3. Get Task Details
- **GET** `/api/{user_id}/tasks/{id}`
- **Response**: 200 OK `Task` OR 404 Not Found

#### 4. Update Task Details
- **PUT** `/api/{user_id}/tasks/{id}`
- **Body**: `{"title": "string", "description": "string", "is_completed": boolean}`
- **Response**: 200 OK `Task` OR 404 Not Found

#### 5. Delete Task
- **DELETE** `/api/{user_id}/tasks/{id}`
- **Response**: 204 No Content OR 404 Not Found

#### 6. Complete Task (Partial Update)
- **PATCH** `/api/{user_id}/tasks/{id}/complete`
- **Body**: `{"is_completed": boolean}`
- **Response**: 200 OK `Task`

### Error Handling

- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: Valid JWT, but `user_id` in URL does not match `sub` claim in Token.
- **404 Not Found**: Resource does not exist OR Resource belongs to another user (Security masking).
- **422 Unprocessable Entity**: Invalid JSON body (e.g., missing title).

### Key Entities

- **Task**: JSON representation of the Task model (ID, Title, Description, Status, Dates).

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of endpoints return correct HTTP status codes (2xx, 4xx).
- **SC-002**: Unauthorized cross-user access attempts (ID Mismatch) result in 403 Forbidden in <10ms.
- **SC-003**: API response time for read operations is <100ms.

## Assumptions & Constraints

- **Constraints**:
    - URL structure `/api/{user_id}/...` is mandatory to make ownership checks explicit at the routing level.
- **Assumptions**:
    - Frontend will handle 401/403 errors by redirecting to login.

## Out of Scope

- GraphQL.
- XML support.
- Bulk API endpoints.
