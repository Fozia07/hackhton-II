# Todo AI Chatbot - Data Model Specification

## Entity Definitions

### Conversation Entity
**Entity Name**: Conversation
**Fields**:
- id (UUID, Primary Key, Required): Unique identifier for the conversation
- user_id (UUID, Foreign Key, Required): Reference to the user who owns this conversation
- title (String, Optional): Auto-generated or user-defined title for the conversation
- created_at (DateTime, Required): Timestamp when conversation was created
- updated_at (DateTime, Required): Timestamp when conversation was last updated
- is_active (Boolean, Required): Whether the conversation is currently active

**Relationships**:
- One-to-Many: Conversation → Messages (conversation_id foreign key in Message table)
- Many-to-One: Conversation ← User (user_id foreign key in Conversation table)

**Validation Rules**:
- user_id must reference an existing user in the system
- created_at and updated_at are automatically managed by the system
- is_active defaults to true when created

### Message Entity
**Entity Name**: Message
**Fields**:
- id (UUID, Primary Key, Required): Unique identifier for the message
- conversation_id (UUID, Foreign Key, Required): Reference to the conversation this message belongs to
- user_id (UUID, Foreign Key, Required): Reference to the user who sent this message
- role (String, Required): Role of the sender ('user' or 'assistant')
- content (Text, Required): The actual message content
- timestamp (DateTime, Required): When the message was sent
- sequence_number (Integer, Required): Order of the message in the conversation

**Relationships**:
- Many-to-One: Message → Conversation (conversation_id foreign key)
- Many-to-One: Message → User (user_id foreign key)
- One-to-Many: Message → AgentInteractions (message_id foreign key in AgentInteraction table)

**Validation Rules**:
- conversation_id must reference an existing conversation owned by the user
- role must be either 'user' or 'assistant'
- content length must be between 1 and 10,000 characters
- sequence_number must be unique within the conversation context

### AgentInteraction Entity
**Entity Name**: AgentInteraction
**Fields**:
- id (UUID, Primary Key, Required): Unique identifier for the interaction
- message_id (UUID, Foreign Key, Required): Reference to the message that triggered this interaction
- user_id (UUID, Foreign Key, Required): Reference to the user who initiated the interaction
- tool_name (String, Required): Name of the MCP tool invoked
- tool_input (JSON, Required): Input parameters passed to the tool
- tool_output (JSON, Required): Output returned by the tool
- timestamp (DateTime, Required): When the interaction occurred
- success (Boolean, Required): Whether the tool invocation succeeded

**Relationships**:
- Many-to-One: AgentInteraction → Message (message_id foreign key)
- Many-to-One: AgentInteraction → User (user_id foreign key)

**Validation Rules**:
- tool_name must be one of the predefined MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- tool_input and tool_output must be valid JSON
- success indicates whether the operation completed without errors

### Task Entity (Enhanced from Phase II)
**Entity Name**: Task (Extended from Phase II)
**Fields**:
- id (UUID, Primary Key, Required): Unique identifier for the task
- user_id (UUID, Foreign Key, Required): Reference to the user who owns this task
- title (String, Required): Title/description of the task
- priority (String, Optional): Priority level ('low', 'medium', 'high')
- due_date (DateTime, Optional): When the task is due
- category (String, Optional): Category classification
- completed (Boolean, Required): Whether the task is completed
- created_at (DateTime, Required): When the task was created
- updated_at (DateTime, Required): When the task was last updated
- completed_at (DateTime, Optional): When the task was completed

**Relationships**:
- Many-to-One: Task → User (user_id foreign key)
- One-to-Many: Task → AgentInteractions (via tool references in AgentInteraction)

**Validation Rules**:
- user_id must reference an existing user
- priority must be one of 'low', 'medium', 'high' if provided
- completed_at must be null if completed is false
- due_date should be in the future if provided

## State Transitions

### Task State Transitions
- **Pending** → **Completed**: When complete_task MCP tool is called
- **Completed** → **Pending**: When update_task MCP tool is called with completed=false
- **Any State** → **Updated**: When update_task MCP tool is called with any field changes

### Conversation State Transitions
- **Active** → **Inactive**: When conversation is archived or closed
- **Inactive** → **Active**: When conversation is reopened (if supported)

## Indexing Strategy
- Conversation table: Index on user_id for efficient user-based queries
- Message table: Composite index on (conversation_id, sequence_number) for ordered retrieval
- Message table: Index on user_id for user-based message queries
- AgentInteraction table: Index on user_id and message_id for efficient lookups
- Task table: Index on user_id and completed for efficient task listing