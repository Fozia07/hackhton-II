# Data Model: Console Todo Application

## Task Entity

### Fields
- **id**: Integer (sequential, starting from 1) - Unique identifier for the task
- **title**: String - Text description of the task
- **completed**: Boolean - Status indicating if the task is completed (True) or pending (False)

### Validation Rules
- **id**: Must be a positive integer, unique within the application session
- **title**: Must be a non-empty string (after trimming whitespace)
- **completed**: Must be a boolean value (True or False)

### State Transitions
- **Pending to Completed**: When user marks task as complete
- **Completed to Pending**: When user marks task as incomplete

### Relationships
- No relationships with other entities (standalone entity)

## Application State

### Fields
- **tasks**: List of Task entities - Collection of all tasks in the current session
- **next_id**: Integer - The next available ID to assign to a new task (starts at 1)

### Constraints
- **Uniqueness**: Each task must have a unique ID within the application
- **Immutability**: Task IDs cannot be changed after creation
- **Persistence**: All data exists only in memory during the application session