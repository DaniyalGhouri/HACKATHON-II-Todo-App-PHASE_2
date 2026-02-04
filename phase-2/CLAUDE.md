# Claude Code Guidelines

## Commands

- **Build**: `uv sync`
- **Test**: `pytest`
- **Run**: `python -m src.cli.main`

## Architecture

- **Models**: `src/models/` (Data entities)
- **Services**: `src/services/` (Business logic)
- **CLI**: `src/cli/` (Interface layer)
- **Lib**: `src/lib/` (Shared utilities)

## Style

- PEP 8
- Type hints required
- TDD workflow (Red-Green-Refactor)
