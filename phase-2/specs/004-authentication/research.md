# Research: Authentication Strategy

## Unknowns & Clarifications

### 1. Better Auth Integration
- **Context**: Need to use Better Auth for Next.js.
- **Decision**: Use `better-auth` library configured with a PostgreSQL adapter.
- **Rationale**: Mandated by Spec/Constitution. Handles complexity of secure password hashing and session management.

### 2. JWT Strategy
- **Context**: How to share auth state with Python Backend?
- **Decision**: 
  - Better Auth handles login and issues a session token.
  - *Correction/Refinement*: Better Auth typically manages sessions. We need a JWT.
  - **Research Result**: Better Auth can be configured to expose the session token or we can use the `better-auth` client to get the session. 
  - **Simplification for Phase II**: We will configure Better Auth to sign tokens using a `BETTER_AUTH_SECRET`. The Python backend will use the SAME secret to verify the signature of the session token (which is essentially a JWT or signed string) sent in the `Authorization` header.
- **Alternatives**: 
  - Call Better Auth API from Python to validate session (Adds latency).
  - Use a separate IDP (Auth0/Clerk) - Excluded by constraints (Better Auth mandated).

### 3. Shared Secret Management
- **Context**: Both services need the secret.
- **Decision**: Store `BETTER_AUTH_SECRET` in `.env` file loaded by both Next.js and FastAPI.
- **Constraint**: Must match exactly.

## Technology Decisions

| Technology | Choice | Reasoning |
| :--- | :--- | :--- |
| **Frontend Auth Lib** | Better Auth | Mandated, modern, typesafe. |
| **Backend Verification** | PyJWT | Standard, robust JWT library for Python. |
| **Token Transport** | Bearer Header | Standard REST pattern. |
| **Hashing** | Scrypt/Argon2 | Managed internally by Better Auth. |

## Patterns

- **Middleware/Dependency**: Python backend will use a FastAPI `Depends(get_current_user)` which extracts the Bearer token, decodes it using `BETTER_AUTH_SECRET`, and returns a user object or raises 401.
