# Data Model: Interactive CLI Experience for Todo App

## EnhancedTaskDisplay Entity

### Fields
- **task**: Task object - The original task being displayed
- **formatted_title**: String - The title formatted for display (with possible styling)
- **visual_status_indicator**: String - Visual representation of completion status (e.g., "✓", "✗", "[x]", "[ ]")
- **display_position**: Integer - Position in the display list for selection purposes

### Validation Rules
- **task**: Must be a valid Task object from the base application
- **formatted_title**: Must be a string that properly represents the original title
- **visual_status_indicator**: Must be a valid status indicator character sequence

### Relationships
- **task**: References the original Task entity from the base application

## UserCommand Entity

### Fields
- **raw_input**: String - The original user input string
- **parsed_command**: String - The normalized command name
- **arguments**: List[String] - List of parsed arguments
- **suggestions**: List[String] - List of potential command suggestions when input is invalid
- **is_valid**: Boolean - Whether the command is recognized and properly formatted

### Validation Rules
- **raw_input**: Must be a non-empty string
- **parsed_command**: Must match one of the recognized command patterns
- **is_valid**: Must be determined based on command recognition and argument validation

### State Transitions
- **Unparsed to Parsed**: When command is successfully parsed
- **Invalid to Valid**: When user corrects an invalid command

### Relationships
- No direct relationships to other entities

## InteractiveSession Entity

### Fields
- **session_id**: String - Unique identifier for the session
- **command_history**: List[String] - History of commands entered in the session
- **current_state**: String - Current interaction state (e.g., "main_menu", "adding_task", "updating_task")
- **selected_task_id**: Integer - ID of currently selected task for operations (null if none)
- **filter_mode**: String - Current task filtering mode ("all", "pending", "completed")

### Validation Rules
- **session_id**: Must be unique within the application runtime
- **current_state**: Must be one of the predefined valid states
- **selected_task_id**: Must be null or reference an existing task

### State Transitions
- **main_menu to adding_task**: When user initiates task addition
- **main_menu to updating_task**: When user selects task for update
- **adding_task to main_menu**: When task addition is completed or cancelled
- **updating_task to main_menu**: When task update is completed or cancelled

### Relationships
- No direct relationships to other entities (interacts with TaskService through the CLI interface)

## DisplayConfiguration Entity

### Fields
- **color_scheme**: String - Color scheme for display (e.g., "default", "high_contrast")
- **show_line_numbers**: Boolean - Whether to show line numbers in task lists
- **compact_mode**: Boolean - Whether to use compact display format
- **show_timestamps**: Boolean - Whether to show timestamps for tasks (if available)

### Validation Rules
- **color_scheme**: Must be one of the supported color schemes
- **show_line_numbers**: Must be boolean
- **compact_mode**: Must be boolean
- **show_timestamps**: Must be boolean

### Relationships
- No relationships with other entities