# Todo AI Chatbot - Phase III Backend

This is the backend for Phase III of the Todo AI Chatbot project, implementing an AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture.

## Architecture Overview

```
┌─────────────────┐ ┌──────────────────────────────────────────────┐ ┌─────────────────┐
│                 │ │ FastAPI Server                              │ │                 │
│                 │ │ ┌────────────────────────────────────────┐   │ │                 │
│   ChatKit UI    │─┼▶│                                        │   │ │  Neon DB        │
│  (Frontend)     │ │ │ Chat Endpoint                          │   │ │ (PostgreSQL)    │
│                 │ │ │ POST /api/chat                         │   │ │                 │
│                 │ │ └───────────────┬────────────────────────┘   │ │ - tasks         │
│                 │ │                 │                            │ │ - conversations   │
│                 │ │                 ▼                            │ │ - messages      │
│                 │ │ ┌────────────────────────────────────────┐   │ └─────────────────┘
│                 │◀┼─│ OpenAI Agents SDK                      │   │                   │
│                 │ │ │ (Agent + Runner)                       │   │                   │
│                 │ │ └───────────────┬────────────────────────┘   │                   │
│                 │ │                 │                            │                   │
│                 │ │                 ▼                            │                   │
│                 │ │ ┌────────────────────────────────────────┐   │                   │
│                 │ │ │ MCP Server                             │   │                   │
│                 │ │ │ (MCP Tools for Task Operations)        │   │                   │
│                 │ │ └────────────────────────────────────────┘   │                   │
└─────────────────┘ └──────────────────────────────────────────────┘ └─────────────────┘
```

## Features Implemented

- **Database Models**: Complete SQLModel models for tasks, conversations, messages, and agent interactions
- **User Scoping**: All operations are properly scoped by user_id for multi-tenancy
- **Async Operations**: Full async support for high-performance operations
- **Migration Support**: Alembic configured for database versioning
- **Utility Functions**: Comprehensive CRUD operations with proper error handling
- **Testing**: Complete test suite for all database operations

## Database Schema

### Task Model
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key)
- `title`: String
- `description`: String (Optional)
- `completed`: Boolean
- `priority`: String (low, medium, high)
- `due_date`: DateTime (Optional)
- `category`: String (Optional)
- `created_at`: DateTime
- `updated_at`: DateTime
- `completed_at`: DateTime (Optional)

### Conversation Model
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key)
- `title`: String (Optional)
- `created_at`: DateTime
- `updated_at`: DateTime
- `is_active`: Boolean

### Message Model
- `id`: UUID (Primary Key)
- `conversation_id`: UUID (Foreign Key)
- `user_id`: UUID (Foreign Key)
- `role`: String (user, assistant)
- `content`: Text
- `sequence_number`: Integer
- `timestamp`: DateTime

### AgentInteraction Model
- `id`: UUID (Primary Key)
- `message_id`: UUID (Foreign Key)
- `user_id`: UUID (Foreign Key)
- `tool_name`: String
- `tool_input`: JSON
- `tool_output`: JSON
- `timestamp`: DateTime
- `success`: Boolean
- `error_message`: String (Optional)

## Installation

1. Clone the repository
2. Navigate to the `phaseIII/backend` directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or with Poetry:
   ```bash
   poetry install
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running Tests

```bash
pytest
```

## Development

This project follows the Spec-Kit Plus methodology with:
- Constitution → Specify → Plan → Tasks → Implement flow
- Complete isolation from Phase II codebase
- Stateless architecture with all state persisted in the database
- MCP tools for AI agent interactions

## Next Steps

1. Implement the MCP server with the required tools (add_task, list_tasks, etc.)
2. Create the FastAPI endpoints for the chat functionality
3. Integrate with OpenAI Agents SDK
4. Build the frontend with OpenAI ChatKit