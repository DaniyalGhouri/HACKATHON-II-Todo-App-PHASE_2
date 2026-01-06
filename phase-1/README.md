# Todo In-Memory Python Console Application

A simple command-line Todo application that stores tasks in memory during runtime.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)

## Setup

1. Clone the repository.
2. Install dependencies using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -e .[dev]
```

## Usage

Run the application module:

```bash
# Add a task
python -m src.cli.main add "Buy milk"

# List tasks
python -m src.cli.main list

# Mark as complete
python -m src.cli.main complete 1

# Update a task
python -m src.cli.main update 1 "Buy oat milk"

# Delete a task
python -m src.cli.main delete 1
```

**Note**: Since data is stored in memory, state is lost between commands. This application serves as a demonstration of clean architecture and CLI structure.

## Testing

Run the test suite:

```bash
pytest
```
