# Phase I: Console Todo Application

A simple, in-memory console-based todo application built with Python. This is Phase I of the multi-phase todo application project.

## Features

- Add, list, update, delete, and mark tasks as complete/incomplete
- In-memory storage (no persistent data)
- Command-line interface
- Sequential task IDs starting from 1
- Runs in a uv-managed virtual environment

## Requirements

- Python 3.8+
- uv (for environment management)

## Setup

1. Make sure you have `uv` installed
2. Clone or download this repository
3. Navigate to the project directory
4. Create and activate the virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```
5. Install the package in development mode:
   ```bash
   uv pip install -e .
   ```

## Usage

Run the application:
```bash
python -m app.todo_app
```

Or if installed with the package script:
```bash
console-todo
```

### Available Commands

- `add "Your task title"` - Add a new task
- `list` or `ls` - List all tasks
- `update <id> "New title"` - Update a task's title
- `delete <id>` - Delete a task
- `complete <id>` or `done <id>` - Mark task as complete
- `incomplete <id>` or `undo <id>` - Mark task as incomplete
- `help` or `?` - Show help
- `exit` or `quit` - Exit the application

## Project Structure

```
app/
├── todo_app.py          # Main application entry point
├── models/
│   └── task.py          # Task model definition
├── services/
│   └── task_service.py  # Task management logic
└── cli/
    └── cli_interface.py # Command-line interface
```

## Architecture

- **Task Model**: Defines the structure of a task with id, title, and completion status
- **Task Service**: Handles in-memory storage and operations for tasks
- **CLI Interface**: Provides command-line interaction for users
- **Main Application**: Orchestrates the components

## Development

The application follows the specification and plan created as part of the spec-driven development process.