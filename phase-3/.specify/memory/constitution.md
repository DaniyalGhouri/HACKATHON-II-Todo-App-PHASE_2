<!--
Sync Impact Report:
- Version change: Template -> 1.0.0
- Modified principles: 
    - [PRINCIPLE_1] -> I. Stateless Architecture
    - [PRINCIPLE_2] -> II. Persistent Conversation History
    - [PRINCIPLE_3] -> III. MCP-Driven AI Logic
    - [PRINCIPLE_4] -> IV. Tool-Based Task Management
    - [PRINCIPLE_5] -> V. UI/Logic Separation
    - [PRINCIPLE_6] -> VI. Secure Multi-Tenancy
    - [PRINCIPLE_7] -> VII. Agentic Dev Workflow
- Added sections: Implementation Constraints, Development Standards
- Removed sections: None
- Templates requiring updates:
    - ✅ .specify/templates/plan-template.md (Referenced in Constitution Check)
    - ✅ .specify/templates/spec-template.md (Requirements alignment)
    - ✅ .specify/templates/tasks-template.md (Workflow alignment)
- Follow-up TODOs: None
-->

# Phase III Todo AI Chatbot Constitution

## Core Principles

### I. Stateless Architecture
The FastAPI backend must not store any conversation state, session data, agent memory, or application state in memory between requests. Every request must be handled independently and must reconstruct all required context from the database.

### II. Persistent Conversation History
All conversation continuity must be achieved through persistent storage. Conversations must be stored in a Conversation table, and every message exchanged between the user and the assistant must be stored in a Message table. The server must reload the entire conversation history from the database on each request.

### III. MCP-Driven AI Logic
The AI logic must be implemented using the OpenAI Agents SDK. The AI agent must not access the database or application services directly. All task-related operations must be performed exclusively through MCP tools exposed by an MCP server implemented using the Official MCP SDK.

### IV. Tool-Based Task Management
The MCP server must expose standardized tools for task creation, listing, updating, completion, and deletion. Each MCP tool must be stateless and must receive all required inputs explicitly, including the authenticated user identifier. MCP tools are the only components permitted to modify task data in the database.

### V. UI/Logic Separation
The frontend must be implemented using OpenAI ChatKit. Its sole responsibility is to provide a conversational user interface and communicate with the backend chat endpoint. It must not contain business logic or task logic.

### VI. Secure Multi-Tenancy
Authentication must be enforced using Better Auth. Every request must be associated with a user_id, and all data access must be scoped to that user. No cross-user data access is permitted.

### VII. Agentic Dev Workflow (NON-NEGOTIABLE)
All development must follow the Agentic Dev Stack workflow in the order: specification, planning, task decomposition, and implementation. Manual coding outside generated artifacts is not allowed.

## Implementation Constraints

- **Backend Framework**: FastAPI (Stateless)
- **AI Agent Framework**: OpenAI Agents SDK
- **MCP Integration**: Official MCP SDK
- **Frontend Framework**: OpenAI ChatKit
- **Authentication**: Better Auth
- **Workflow Tools**: Claude Code, Spec-Kit Plus

## Development Standards

- All changes must be small, testable, and reference code precisely.
- Every user prompt must be recorded in a Prompt History Record (PHR).
- Architectural Decision Records (ADR) must be suggested for significant decisions.
- High-quality tests must be added for all features and bug fixes.

## Governance

This constitution is binding and governs all architectural, design, and implementation decisions without exception. All pull requests and code reviews must verify compliance with these principles.

### Amendment Procedure
Amendments to this constitution require documentation of the rationale and a version bump according to semantic versioning rules:
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions.
- **MINOR**: New principle/section added or materially expanded guidance.
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements.

**Version**: 1.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08