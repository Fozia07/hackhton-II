# MCP Tools Contract

**Service**: MCP Server
**Base URL**: `http://mcp-server:8002`
**Protocol**: MCP over HTTP (streamable-http transport)
**Date**: 2026-02-13

## Overview

MCP (Model Context Protocol) server exposing 5 tools for task management. Used by OpenAI Agents SDK to enable AI assistant task operations.

## MCP Protocol Basics

**Transport**: `streamable-http` (compatible with OpenAI Agents SDK)
**Encoding**: JSON-RPC 2.0 over HTTP
**Content-Type**: `application/json`

**Tool Discovery**:
```json
POST /
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Tool Invocation**:
```json
POST /
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "add_task",
    "arguments": {
      "user_id": "user_123",
      "title": "Buy groceries"
    }
  }
}
```

## Registered Tools

### 1. add_task

**Purpose**: Create a new task for the authenticated user in the database

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | string | ✅ Yes | The ID of the user creating the task |
| `title` | string | ✅ Yes | The title/description of the task to be created |
| `description` | string | ❌ No | Additional details about the task |

**Returns**:
```json
{
  "task_id": "task_456",
  "status": "created",
  "title": "Buy groceries"
}
```

**Error Responses**:
- **Invalid user_id**: `{"error": "User not found", "code": "USER_NOT_FOUND"}`
- **Empty title**: `{"error": "Title is required", "code": "VALIDATION_ERROR"}`

**Example Usage** (via MCP):
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add_task",
    "arguments": {
      "user_id": "user_123",
      "title": "Buy groceries",
      "description": "Milk, bread, eggs"
    }
  }
}
```

---

### 2. list_tasks

**Purpose**: Retrieve all tasks for the authenticated user with optional filtering by status

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | string | ✅ Yes | The ID of the user whose tasks to retrieve |
| `status` | string | ❌ No | Filter tasks by completion status ('all', 'pending', 'completed') |

**Returns**:
```json
[
  {
    "id": "task_456",
    "title": "Buy groceries",
    "completed": false,
    "priority": "medium",
    "due_date": "2026-02-15",
    "category": "personal",
    "created_at": "2026-02-13T10:00:00Z",
    "updated_at": "2026-02-13T10:00:00Z",
    "completed_at": null
  },
  {
    "id": "task_789",
    "title": "Finish report",
    "completed": true,
    "priority": "high",
    "due_date": "2026-02-14",
    "category": "work",
    "created_at": "2026-02-12T09:00:00Z",
    "updated_at": "2026-02-13T11:00:00Z",
    "completed_at": "2026-02-13T11:00:00Z"
  }
]
```

**Status Filter Values**:
- `all` - Return all tasks (default)
- `pending` - Return only incomplete tasks
- `completed` - Return only completed tasks

**Error Responses**:
- **Invalid user_id**: `{"error": "User not found", "code": "USER_NOT_FOUND"}`
- **Invalid status**: `{"error": "Invalid status filter", "code": "VALIDATION_ERROR"}`

---

### 3. complete_task

**Purpose**: Mark a specific task as completed for the authenticated user

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | string | ✅ Yes | The ID of the user attempting to complete the task |
| `task_id` | string | ✅ Yes | The ID of the task to mark as completed |

**Returns**:
```json
{
  "task_id": "task_456",
  "status": "completed",
  "title": "Buy groceries"
}
```

**Error Responses**:
- **Task not found**: `{"error": "Task not found", "code": "TASK_NOT_FOUND"}`
- **Unauthorized**: `{"error": "Task does not belong to user", "code": "UNAUTHORIZED"}`
- **Already completed**: `{"error": "Task already completed", "code": "ALREADY_COMPLETED"}`

---

### 4. delete_task

**Purpose**: Remove a specific task from the user's task list

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | string | ✅ Yes | The ID of the user attempting to delete the task |
| `task_id` | string | ✅ Yes | The ID of the task to delete |

**Returns**:
```json
{
  "task_id": "task_456",
  "status": "deleted",
  "title": "Buy groceries"
}
```

**Error Responses**:
- **Task not found**: `{"error": "Task not found", "code": "TASK_NOT_FOUND"}`
- **Unauthorized**: `{"error": "Task does not belong to user", "code": "UNAUTHORIZED"}`

---

### 5. update_task

**Purpose**: Modify properties of an existing task for the authenticated user

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `user_id` | string | ✅ Yes | The ID of the user attempting to update the task |
| `task_id` | string | ✅ Yes | The ID of the task to update |
| `title` | string | ❌ No | New title for the task |
| `description` | string | ❌ No | New description for the task |
| `completed` | boolean | ❌ No | New completion status for the task |

**Returns**:
```json
{
  "task_id": "task_456",
  "status": "updated",
  "title": "Buy groceries and cook dinner"
}
```

**Error Responses**:
- **Task not found**: `{"error": "Task not found", "code": "TASK_NOT_FOUND"}`
- **Unauthorized**: `{"error": "Task does not belong to user", "code": "UNAUTHORIZED"}`
- **Validation error**: `{"error": "Title cannot be empty", "code": "VALIDATION_ERROR"}`

**Update Rules**:
- At least one optional parameter must be provided
- Partial updates allowed (only provided fields are changed)
- Empty strings not allowed for title
- Completed status change logs completion timestamp

---

## Server Configuration

**From `phaseIV/backend/app/mcp_server/config.py`**:

```python
SERVER_NAME = "todo-ai-chatbot-mcp-server"
SERVER_VERSION = "1.0.0"
TRANSPORT_TYPE = "streamable-http"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8002
REGISTERED_TOOLS = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task"
]
```

## Authentication

**Current Implementation**: User ID passed as parameter (trust-based)

**Security Notes**:
- MCP server runs in internal cluster network (not exposed externally)
- Backend service authenticates users before calling MCP tools
- User ID validation happens in tool implementation (checks against database)
- Future enhancement: JWT token validation at MCP server level

## Backend Integration

**Backend Service** calls MCP server for chatbot requests:

```python
# Example from phaseIV/backend/app/services/chatbot_service.py
import httpx

async def call_mcp_tool(tool_name: str, arguments: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://mcp-server:8002/",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=5.0
        )
        return response.json()
```

**DNS Resolution**: `mcp-server` resolves to Service ClusterIP within `todo-chatbot` namespace

## Error Handling

**MCP Protocol Errors**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": {
      "details": "user_id is required"
    }
  }
}
```

**Tool Execution Errors**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "error": "Task not found",
    "code": "TASK_NOT_FOUND",
    "task_id": "invalid_id"
  }
}
```

## Testing

### Connectivity Test (from backend pod)

```bash
kubectl exec -n todo-chatbot <backend-pod> -- curl -X POST http://mcp-server:8002/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**Expected Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "add_task", "description": "Create a new task..."},
      {"name": "list_tasks", "description": "Retrieve all tasks..."},
      {"name": "complete_task", "description": "Mark a task as completed..."},
      {"name": "delete_task", "description": "Remove a task..."},
      {"name": "update_task", "description": "Modify task properties..."}
    ]
  }
}
```

### Tool Invocation Test

```bash
kubectl exec -n todo-chatbot <backend-pod> -- curl -X POST http://mcp-server:8002/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"list_tasks",
      "arguments":{"user_id":"test_user"}
    }
  }'
```

## Performance Expectations

**Response Times**:
- Tool listing: <100ms
- add_task: <500ms (database write)
- list_tasks: <300ms (database query)
- complete_task: <400ms (database update)
- delete_task: <400ms (database delete)
- update_task: <400ms (database update)

**Concurrency**: Handles up to 100 concurrent requests per pod
**Resource Usage**: <200m CPU, <256Mi memory per pod under normal load

## Summary

The MCP server exposes 5 task management tools via JSON-RPC protocol:
1. **add_task** - Create tasks
2. **list_tasks** - Query tasks with filtering
3. **complete_task** - Mark tasks done
4. **delete_task** - Remove tasks
5. **update_task** - Modify task properties

All tools require `user_id` for authentication and authorization. Server runs on port 8002 with `streamable-http` transport compatible with OpenAI Agents SDK.
