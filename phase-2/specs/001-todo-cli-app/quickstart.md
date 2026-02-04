# Quickstart: Todo In-Memory CLI

**Feature Branch**: `001-todo-cli-app`

## Prerequisites

- Python 3.13+ installed.
- Terminal / Command Prompt.

## Setup

1. Clone the repository.
2. Navigate to project root.

## Running Tests

Execute all tests using pytest:

```bash
pytest
```

## Running the Application

The application entry point is `src/cli/main.py` (or as defined in tasks).

**Usage Examples**:

```bash
# Add
python -m src.cli.main add "Buy milk"

# List
python -m src.cli.main list

# Complete
python -m src.cli.main complete 1
```

## Development

- Source code in `src/`.
- Tests in `tests/`.
- Follow "Red-Green-Refactor": Write test first, see it fail, implement logic, pass.
