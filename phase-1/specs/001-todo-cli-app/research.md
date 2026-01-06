# Research & Decisions: Todo In-Memory Python Console Application

**Feature Branch**: `001-todo-cli-app`
**Date**: 2026-01-06

## Decisions

### 1. CLI Argument Parsing
**Decision**: Use Python's standard library `argparse`.
**Rationale**: 
- Constitution mandates minimal external dependencies.
- `argparse` is built-in, robust, and handles subcommands (add, list, etc.) effectively.
- Meets "Pure CLI Architecture" principle.

**Alternatives Considered**:
- `click`: External dependency, adds complexity not needed for this scope.
- `sys.argv`: Too manual, hard to handle validation and help messages nicely.

### 2. Data Structure
**Decision**: Use Python `dataclasses` for the Task entity and a simple `list` of objects for storage.
**Rationale**:
- `dataclasses` provide a clean, type-safe way to define entities (Python 3.7+ feature).
- In-memory constraint means no complex ORM is needed.
- A list allows simple iteration; a dictionary mapping ID -> Task could optimize lookups if needed, but for Phase I scope (100 tasks), a list or dict is negligible. Will use `dict` for O(1) ID lookups.

**Alternatives Considered**:
- `sqlite3` in-memory: Overkill for simple list logic, adds SQL complexity.
- Raw dictionaries: Less type safety, harder to maintain.

### 3. Testing Framework
**Decision**: Use `pytest`.
**Rationale**:
- Industry standard for Python.
- Supports fixtures which are great for resetting in-memory state between tests.
- "Test-First Rigor" principle aligned.

## Open Questions

- None. All clarifications resolved in Spec.
