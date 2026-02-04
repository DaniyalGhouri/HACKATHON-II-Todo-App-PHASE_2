<!--
SYNC IMPACT REPORT
Version: 1.0.0 -> 2.0.0
Modified Principles:
- Pure CLI Architecture -> Full-Stack Web Architecture
- In-Memory Persistence -> Modern Data Layer
- Clean Code & Modern Python -> Clean Code & Standards
Added Sections:
- Authentication & Security
Templates Status:
- plan-template.md: ✅ Aligned
- spec-template.md: ✅ Aligned
- tasks-template.md: ✅ Aligned
-->
# Spec-Kit Constitution

## Core Principles

### I. Spec-Driven Development
The Specification is the single source of truth. Code is a derived artifact. The flow of change is strictly unidirectional: Constitution → Spec → Plan → Tasks → Code. Implementation never precedes specification. All changes must be traceable to specs.

### II. Full-Stack Web Architecture
The system is designed as a Full-Stack Web Application.
- Architecture must support multi-user isolation.
- Communication via REST API only (no RPC or GraphQL).
- Clear separation between Frontend and Backend concerns.

### III. Modern Data Layer
Data persistence is handled by robust, serverless infrastructure.
- Database must be Neon Serverless PostgreSQL.
- No local file-based storage for domain entities in production.

### IV. Authentication & Security
Security is foundational and non-negotiable.
- JWT authentication required for all API access.
- Backend must verify JWT independently.
- Frontend uses Better Auth for authentication management.

### V. Agent-Exclusive Implementation
The Human defines the "What" (Spec/Review); the Agent implements the "How" (Code/Test).
- Manual code editing is forbidden.
- All features and changes are implemented by the Agent tools.

### VI. Test-First Rigor
No logic is written without a failing test (Red-Green-Refactor).
- Unit tests for all business logic.
- Integration tests for API endpoints.
- 100% pass rate required for "Done".

## Technical Constraints

- **Project**: Hackathon Phase II – Todo Full-Stack Web App
- **Database**: Neon Serverless PostgreSQL
- **API Style**: REST
- **Auth**: JWT (Backend verify), Better Auth (Frontend)
- **Environment**: Win32

## Development Workflow

1.  **Clarify**: User defines goals.
2.  **Spec**: Agent drafts detailed requirements (`/sp.specify`).
3.  **Plan**: Agent architects the solution (`/sp.plan`).
4.  **Task**: Agent breaks down work (`/sp.tasks`).
5.  **Implement**: Agent writes tests and code (`/sp.implement` / tools).
6.  **Verify**: Automated test suites + User acceptance.

## Governance

This Constitution serves as the primary governance document for the Hackathon Phase II project.
- **Amendments**: Changes to principles require a Pull Request and explicit user approval.
- **Supremacy**: In conflicts between code and constitution, the constitution prevails.
- **Definition of Done**: A feature is Done when it is Specified, Tested, Implemented, Verified, and Documented.

**Version**: 2.0.0 | **Ratified**: 2026-01-06 | **Last Amended**: 2026-01-19