# Data Model: Dashboard UI Redesign

**Feature**: Dashboard UI Redesign
**Branch**: 019-dashboard-ui-redesign
**Created**: 2026-01-15

## Entity Definitions

### Task
Represents a user's task item in the system.

**Fields**:
- `id` (Integer): Unique identifier for the task
- `title` (String): Title or name of the task (required)
- `description` (String | null): Optional detailed description of the task
- `completed` (Boolean): Whether the task is completed (default: false)
- `due_date` (DateTime | null): Due date for the task (nullable)
- `created_at` (DateTime): Timestamp when the task was created
- `updated_at` (DateTime): Timestamp when the task was last updated

**Validation Rules**:
- Title must not be empty
- Title length: 1-255 characters
- Description length: 0-1000 characters
- Due date must be in the future (if provided)

**State Transitions**:
- `incomplete` → `completed`: When user marks task as complete
- `completed` → `incomplete`: When user unmarks task as complete

### TaskFilter
Represents the current filter state for task display.

**Fields**:
- `status` (Enum): Current status filter ("all", "today", "pending", "overdue")
- `search_query` (String | null): Optional search term to filter tasks
- `sort_order` (Enum): Sort order ("asc", "desc") by creation date

**Validation Rules**:
- Status must be one of the allowed values
- Search query length: 0-100 characters

## Relationships

### Task to User
- **Relationship**: Many-to-One
- **Description**: Each task belongs to a single user
- **Constraint**: Task cannot exist without a user

## UI State Models

### TabState
Represents the current active tab in the dashboard UI.

**Fields**:
- `active_tab` (Enum): Current active tab ("today", "pending", "overdue")
- `tab_counts` (Object): Count of tasks in each tab category

### TaskViewState
Represents the current view state for task display.

**Fields**:
- `selected_task_id` (Integer | null): ID of currently selected task for editing
- `show_add_form` (Boolean): Whether the add task form is visible
- `filter_applied` (Boolean): Whether a filter is currently applied

## Constraints and Business Rules

### Data Integrity
- Task titles must be unique within user's tasks (case-insensitive)
- Completed tasks cannot have due dates in the past
- Tasks must belong to authenticated users

### Validation
- All required fields must be present
- Field lengths must conform to defined limits
- Dates must be valid date/time values
- Status values must be from allowed enum values

## Indexes

### Task Table
- Primary index on `id`
- Index on `user_id` for efficient user-based queries
- Index on `completed` for filtering completed tasks
- Index on `due_date` for date-based filtering
- Composite index on `(user_id, completed, due_date)` for combined queries

### Performance Considerations
- Queries filtered by user_id will be efficient
- Sorting by creation date will be efficient
- Combined filters (user + completion status + date) will be efficient