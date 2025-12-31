# Quickstart: Console Todo Application

## Setup

1. Ensure you have Python and uv installed on your system
2. Navigate to the project directory
3. Initialize the uv virtual environment:
   ```bash
   uv venv
   ```
4. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate     # On Windows
   ```
5. Install any required dependencies (if pyproject.toml exists):
   ```bash
   uv pip install -e .
   ```

## Running the Application

1. Execute the main application file:
   ```bash
   python app/todo_app.py
   ```

## Using the Application

### Available Commands

- **Add a task**: `add "Your task title here"`
- **List all tasks**: `list` or `ls`
- **Update a task**: `update <id> "New title"`
- **Delete a task**: `delete <id>`
- **Mark task as complete**: `complete <id>` or `done <id>`
- **Mark task as incomplete**: `incomplete <id>` or `undo <id>`
- **Show help**: `help` or `?`
- **Exit application**: `exit` or `quit`

### Example Usage

```
> add "Buy groceries"
Task 1 added: Buy groceries [PENDING]

> add "Walk the dog"
Task 2 added: Walk the dog [PENDING]

> list
1. [ ] Buy groceries
2. [ ] Walk the dog

> complete 1
Task 1 marked as complete

> list
1. [x] Buy groceries
2. [ ] Walk the dog

> update 2 "Walk the cat"
Task 2 updated to: Walk the cat

> delete 2
Task 2 deleted

> list
1. [x] Buy groceries
```

## Error Handling

The application will display helpful error messages for:
- Invalid commands
- Non-existent task IDs
- Empty task titles
- Malformed command syntax