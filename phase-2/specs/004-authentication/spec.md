# Feature Specification: Authentication

**Feature Branch**: `004-authentication`
**Created**: 2026-01-19
**Status**: Draft
**Input**: User description: "Create a full authentication feature specification using Better Auth and JWT..."

## User Scenarios & Testing

### User Story 1 - User Signup & Login (Priority: P1)

As a new user, I want to sign up and log in using my email so that I can access the application securely.

**Why this priority**: Application entry point; required for all subsequent interactions.

**Independent Test**:
- Open the application login page.
- Enter email/password (Better Auth UI).
- Submit form.
- Verify JWT is received and stored in browser (LocalStorage/Cookie).
- Verify user is redirected to the dashboard.

**Acceptance Scenarios**:

1. **Given** a new user, **When** they sign up with a valid email/password, **Then** a user record is created in the database.
2. **Given** an existing user, **When** they log in with correct credentials, **Then** a valid JWT is issued.
3. **Given** invalid credentials, **When** logging in, **Then** an error message is displayed.

---

### User Story 2 - Authenticated API Access (Priority: P1)

As a frontend application, I want to attach a JWT to every API request so that the backend can verify the user's identity.

**Why this priority**: Ensures backend security and data isolation.

**Independent Test**:
- Log in to obtain a valid JWT.
- Make a request to a protected endpoint (e.g., `/tasks`) with `Authorization: Bearer <token>`.
- Verify 200 OK response.
- Make the same request without the header.
- Verify 401 Unauthorized response.

**Acceptance Scenarios**:

1. **Given** a valid JWT, **When** accessing a protected API endpoint, **Then** the request is allowed and `request.user` is populated.
2. **Given** an expired or invalid JWT, **When** accessing a protected API endpoint, **Then** the backend returns 401 Unauthorized.

---

### User Story 3 - Session Persistence (Priority: P2)

As a user, I want to remain logged in when I refresh the page so that I don't have to re-enter my credentials constantly.

**Why this priority**: Critical for User Experience.

**Independent Test**:
- Log in.
- Refresh the browser page.
- Verify the user session remains active (JWT still present/valid).
- Verify no redirect to login page occurs.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they reload the page, **Then** the application checks for an existing token and bypasses login if valid.
2. **Given** a user with an expired token, **When** they reload the page, **Then** they are redirected to the login screen.

## Requirements

### Functional Requirements

- **FR-001**: Frontend MUST use **Better Auth** library for handling Signup and Login flows.
- **FR-002**: Backend MUST issue a signed **JWT (JSON Web Token)** upon successful authentication.
- **FR-003**: Frontend MUST store the JWT securely (HttpOnly Cookie preferred, or LocalStorage if necessary for Phase II constraints).
- **FR-004**: Frontend MUST attach the JWT to the `Authorization` header (`Bearer <token>`) for all requests to the Python Backend.
- **FR-005**: Backend MUST independently verify the JWT signature using a shared secret.
- **FR-006**: Backend MUST extract the User ID from the JWT `sub` claim to identify the user.
- **FR-007**: Backend MUST reject any request with a missing, invalid, or expired token with HTTP 401.

### Key Entities

- **User**:
    - `id`: Unique Identifier (UUID).
    - `email`: String (Unique, Required).
    - `password_hash`: String (Managed by Better Auth/Backend).
    - `created_at`: Timestamp.
    - `last_login`: Timestamp.

## Success Criteria

### Measurable Outcomes

- **SC-001**: User can complete Signup/Login flow in under 5 seconds.
- **SC-002**: 100% of protected API endpoints reject requests without a valid JWT.
- **SC-003**: JWT token payload successfully decodes to the correct User ID on the backend.
- **SC-004**: Frontend automatically redirects unauthenticated users to `/login`.

## Assumptions & Constraints

- **Constraints**: 
    - Shared Secret MUST be configured in `.env` for both Frontend (Next.js) and Backend (FastAPI) to verify tokens.
    - No multi-factor authentication (MFA).
- **Assumptions**:
    - Better Auth handles password hashing and storage securely.
    - HTTPS is used in production (HTTP allowed for local dev).

## Out of Scope

- Social Login (Google, GitHub, etc.).
- Password Reset / Forgot Password flows.
- Multi-Factor Authentication (MFA).
- Role-Based Access Control (Admin/User roles).
