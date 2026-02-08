# Research: Phase III Todo AI Chatbot

## Decision 1: AI Agent Framework
- **Decision**: Use `openai-agents` (OpenAI Agents SDK).
- **Rationale**: Specifically designed for building autonomous agents with tool-calling capabilities and structured message management. It integrates well with OpenAI models.
- **Alternatives considered**: LangChain (rejected as too heavyweight for this stateless requirement), direct OpenAI API (rejected to gain structured tool handling).

## Decision 2: MCP Server Implementation
- **Decision**: Use `mcp` Python SDK with `FastMCP`.
- **Rationale**: `FastMCP` provides a decorator-based approach (`@mcp.tool()`) that simplifies tool registration and automatically generates JSON schemas from Python type hints and docstrings.
- **Alternatives considered**: Manual implementation of MCP protocol handlers (rejected as inefficient).

## Decision 3: Database & ORM
- **Decision**: SQLModel with Neon Serverless PostgreSQL.
- **Rationale**: SQLModel provides a clean, type-safe interface that combines Pydantic and SQLAlchemy. Neon supports serverless scaling and provides the required persistence.
- **Alternatives considered**: Raw SQLAlchemy (rejected for lack of native Pydantic integration), Prisma (rejected to stay within the Python ecosystem).

## Decision 4: Frontend Chat Interface
- **Decision**: OpenAI ChatKit.
- **Rationale**: Requirement for Phase III. Provides a high-quality, hosted conversational UI that connects to a custom backend.
- **Alternatives considered**: Custom React chat UI (rejected due to specific requirement).

## Decision 5: Stateless History Management
- **Decision**: Reload full history from `Message` table per request.
- **Rationale**: Directly mandated by the Phase III constitution to ensure horizontal scalability and statelessness.
- **Alternatives considered**: Redis-based session storage (rejected by constitution).
