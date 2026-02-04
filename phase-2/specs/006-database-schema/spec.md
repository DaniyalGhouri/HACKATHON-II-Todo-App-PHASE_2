# Feature Specification: Database Schema

**Feature Branch**: `006-database-schema`
**Created**: 2026-01-19
**Status**: Draft
**Input**: User description: "Define the database schema for Phase II..."

## User Scenarios & Testing

### User Story 1 - Optimized Data Access (Priority: P1)

As a backend developer, I want a schema with proper indexing so that user-filtered queries are efficient at scale.

**Why this priority**: Performance foundation.

**Independent Test**:
- Inspect the generated SQL migration/schema.
- Verify indexes exist on `user_id` and `is_completed`.
- Run `EXPLAIN ANALYZE` on a query filtering by `user_id` (Requires DB access).

**Acceptance Scenarios**:

1. **Given** the `tasks` table, **When** creating the schema, **Then** an index on `user_id` is created automatically.
2. **Given** a query for user tasks, **When** executed, **Then** it uses the `user_id` index.

---

### User Story 2 - Data Integrity (Priority: P1)

As a system architect, I want strict foreign key relationships so that orphaned data is prevented.

**Why this priority**: Data quality.

**Independent Test**:
- Try to insert a Task with a non-existent `user_id`.
- Verify database rejects the insert (Foreign Key Constraint violation).

**Acceptance Scenarios**:

1. **Given** a `tasks` table, **When** `user_id` references the `users` table (managed by auth system/conceptually), **Then** ensure data types match (UUID/String).

## Requirements

### Functional Requirements

- **FR-001**: System MUST define a `tasks` table for persisting Todo items.
- **FR-002**: `tasks` table MUST have a Primary Key `id`.
- **FR-003**: `tasks` table MUST have a Foreign Key `user_id` referencing the User entity (Auth System).
- **FR-004**: System MUST index `tasks.user_id` for efficient multi-tenant queries.
- **FR-005**: System MUST index `tasks.is_completed` for status filtering.
- **FR-006**: Timestamps (`created_at`, `updated_at`) MUST be automatically managed.

### Key Entities

#### Table: `tasks`

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | UUID/Integer | PK, Not Null | Unique identifier |
| `user_id` | String/UUID | FK, Not Null, Indexed | Owner identifier (from Auth) |
| `title` | Text | Not Null | Task title |
| `description` | Text | Nullable | Task details |
| `is_completed` | Boolean | Default `False`, Indexed | Completion status |
| `created_at` | Timestamp | Default `Now()` | Creation time |
| `updated_at` | Timestamp | Default `Now()` | Last update time |

#### Table: `users` (External Reference)
*Note: Managed by Better Auth / Authentication System. Referenced here for integrity context.*
- `id` (PK)
- `email`
- ...

## Success Criteria

### Measurable Outcomes

- **SC-001**: Schema creation script runs without errors on Neon PostgreSQL.
- **SC-002**: Queries filtering by `user_id` execute in <10ms (Index usage).
- **SC-003**: `tasks` table supports >100,000 records without performance degradation on indexed queries.

## Assumptions & Constraints

- **Constraints**:
    - `user_id` format MUST match the ID format issued by Better Auth (String or UUID).
- **Assumptions**:
    - We are using SQLModel (SQLAlchemy) to define this schema in code.

## Out of Scope

- Database stored procedures.
- Complex triggers.
- Views.
