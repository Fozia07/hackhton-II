# Data Model: TODO App Implementation

## Todo Entity

**Definition**: Represents a user's task with title, description, completion status, and timestamps

**Fields**:
- `id`: number - Unique identifier for the todo
- `title`: string - Title of the todo (required, 1-200 characters)
- `description`: string | null - Optional description of the todo (max 1000 characters)
- `completed`: boolean - Completion status flag (default: false)
- `user_id`: number - Foreign key linking to the user who owns this todo
- `created_at`: string - ISO 8601 timestamp of creation
- `updated_at`: string - ISO 8601 timestamp of last update

## TodoCreate Schema

**Definition**: Schema for creating new TODO items

**Fields**:
- `title`: string - Title of the todo (required, 1-200 characters)
- `description`: string | null - Optional description of the todo (max 1000 characters)

## TodoUpdate Schema

**Definition**: Schema for updating existing TODO items

**Fields**:
- `title`: string | null - Updated title of the todo (1-200 characters, optional)
- `description`: string | null - Updated description of the todo (max 1000 characters, optional)
- `completed`: boolean | null - Updated completion status (optional)

## TodoRead Schema

**Definition**: Schema for reading TODO data with user association

**Fields**:
- `id`: number - Unique identifier for the todo
- `title`: string - Title of the todo
- `description`: string | null - Description of the todo
- `completed`: boolean - Completion status flag
- `user_id`: number - Foreign key linking to the user who owns this todo
- `created_at`: string - ISO 8601 timestamp of creation
- `updated_at`: string - ISO 8601 timestamp of last update

## Todo Action

**Definition**: Actions that can be dispatched to the TODO reducer

**Fields**:
- `type`: string - Action type identifier
- `payload`: any (optional) - Additional data for the action

## Todo Context State

**Definition**: Structure holding the current TODO state across the application

**Fields**:
- `todos`: TodoRead[] - Array of user's todo items
- `isLoading`: boolean - Flag indicating TODO operations are in progress
- `error`: string | null - Error message if TODO operation failed
- `selectedTodo`: TodoRead | null - Currently selected todo for editing

## Todo Form Props

**Definition**: Properties for the TodoForm component

**Fields**:
- `onSubmit`: Function - Callback function when form is submitted
- `initialValues`: TodoUpdate | null - Initial values for editing existing todo
- `isSubmitting`: boolean - Flag indicating form submission is in progress