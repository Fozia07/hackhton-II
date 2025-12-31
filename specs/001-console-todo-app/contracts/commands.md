# Command Contracts: Console Todo Application

## Command Interface

### Add Task
- **Command**: `add "task title"`
- **Input**: Task title as string in quotes
- **Success Response**: Task added with assigned ID
- **Error Responses**:
  - Empty title: "Error: Task title cannot be empty"
  - Invalid format: "Error: Please provide a title in quotes"

### List Tasks
- **Command**: `list` or `ls`
- **Input**: None
- **Success Response**: Formatted list of all tasks with ID, status, and title
- **Error Responses**: None

### Update Task
- **Command**: `update <id> "new title"`
- **Input**: Task ID (integer) and new title in quotes
- **Success Response**: Task updated confirmation
- **Error Responses**:
  - Invalid ID: "Error: Task with ID <id> not found"
  - Empty title: "Error: Task title cannot be empty"
  - Invalid format: "Error: Please provide ID and new title"

### Delete Task
- **Command**: `delete <id>`
- **Input**: Task ID (integer)
- **Success Response**: Task deleted confirmation
- **Error Responses**:
  - Invalid ID: "Error: Task with ID <id> not found"

### Complete Task
- **Command**: `complete <id>` or `done <id>`
- **Input**: Task ID (integer)
- **Success Response**: Task marked as complete confirmation
- **Error Responses**:
  - Invalid ID: "Error: Task with ID <id> not found"

### Incomplete Task
- **Command**: `incomplete <id>` or `undo <id>`
- **Input**: Task ID (integer)
- **Success Response**: Task marked as incomplete confirmation
- **Error Responses**:
  - Invalid ID: "Error: Task with ID <id> not found"

### Help
- **Command**: `help` or `?`
- **Input**: None
- **Success Response**: List of available commands
- **Error Responses**: None

### Exit
- **Command**: `exit` or `quit`
- **Input**: None
- **Success Response**: Application terminates
- **Error Responses**: None