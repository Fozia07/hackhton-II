# Test Curl Commands for Conversation Management

## Prerequisites
- Backend server running on http://localhost:8000
- Valid JWT token for authentication
- Replace `YOUR_JWT_TOKEN` with actual token

## Test 1: New Conversation
Create a new conversation by calling the endpoint with no conversation_id:

```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi, I want to add a task to buy groceries"
  }'
```

**Expected Output:**
- Status: 200 OK
- Response body contains:
  - `success`: true
  - `conversation_id`: new UUID string
  - `response`: AI-generated response confirming task addition
  - `tool_calls`: Array with add_task tool call

## Test 2: Continue Existing Conversation
Continue an existing conversation by providing a valid conversation_id:

```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "EXISTING_CONVERSATION_ID",
    "message": "What tasks do I have?"
  }'
```

**Expected Output:**
- Status: 200 OK
- Response body contains:
  - `success`: true
  - `conversation_id`: Same as provided in request
  - `response`: AI-generated response listing tasks
  - `tool_calls`: Array with list_tasks tool call

## Test 3: Error Case (Invalid Task ID)
Test error handling when trying to operate on a non-existent task:

```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "EXISTING_CONVERSATION_ID",
    "message": "Complete task with ID: nonexistent_task_123"
  }'
```

**Expected Output:**
- Status: 200 OK (operation successful, but task not found)
- Response body contains:
  - `success`: true
  - `conversation_id`: Same as provided in request
  - `response`: Friendly error message like "Couldn't find that task, sorry!"
  - `tool_calls`: Array with attempted complete_task call that resulted in error

## Test 4: Authentication Failure
Test with invalid JWT token:

```bash
curl -X POST "http://localhost:8000/api/user123/chat" \
  -H "Authorization: Bearer INVALID_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test message"
  }'
```

**Expected Output:**
- Status: 401 Unauthorized
- Response body contains error message about authentication failure

## Test 5: Cross-User Access Attempt
Test attempting to access another user's conversation:

```bash
curl -X POST "http://localhost:8000/api/other_user_id/chat" \
  -H "Authorization: Bearer YOUR_VALID_JWT_TOKEN_FOR_DIFFERENT_USER" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "ANOTHER_USERS_CONVERSATION_ID",
    "message": "Test message"
  }'
```

**Expected Output:**
- Status: 403 Forbidden
- Response body contains error message about insufficient permissions