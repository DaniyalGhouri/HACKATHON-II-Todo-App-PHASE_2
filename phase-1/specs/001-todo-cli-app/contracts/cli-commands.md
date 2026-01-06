# CLI Interface Contracts

**Feature Branch**: `001-todo-cli-app`

This document defines the inputs (arguments) and outputs (stdout/stderr) for the application.

## 1. Add Task

**Usage**: `todo add <description>`

- **Arguments**:
  - `description` (string, required): Text of the task.
- **Success Output (stdout)**:
  - `Task added. ID: <id>`
- **Error Output (stderr)**:
  - Empty description: `Error: Description cannot be empty.`

## 2. List Tasks

**Usage**: `todo list`

- **Arguments**: None.
- **Success Output (stdout)**:
  - Header: `ID  Status  Description`
  - Rows: `<id> [<x| >] <description>`
  - Example:
    ```text
    1  [ ] Buy milk
    2  [x] Walk dog
    ```
  - If empty: `No tasks found.`

## 3. Update Task

**Usage**: `todo update <id> <description>`

- **Arguments**:
  - `id` (int, required): ID of task to update.
  - `description` (string, required): New text.
- **Success Output (stdout)**:
  - `Task <id> updated.`
- **Error Output (stderr)**:
  - ID not found: `Error: Task ID <id> not found.`
  - Invalid ID format: `Error: ID must be a number.`

## 4. Delete Task

**Usage**: `todo delete <id>`

- **Arguments**:
  - `id` (int, required): ID of task to remove.
- **Success Output (stdout)**:
  - `Task <id> deleted.`
- **Error Output (stderr)**:
  - ID not found: `Error: Task ID <id> not found.`

## 5. Mark Complete

**Usage**: `todo complete <id>`

- **Arguments**:
  - `id` (int, required).
- **Success Output (stdout)**:
  - `Task <id> marked complete.`
- **Error Output (stderr)**:
  - ID not found: `Error: Task ID <id> not found.`

## 6. Mark Incomplete

**Usage**: `todo incomplete <id>`

- **Arguments**:
  - `id` (int, required).
- **Success Output (stdout)**:
  - `Task <id> marked incomplete.`
- **Error Output (stderr)**:
  - ID not found: `Error: Task ID <id> not found.`
