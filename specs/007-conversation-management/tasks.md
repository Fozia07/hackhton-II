# Implementation Tasks: Finalize Conversation Management + Polish

## Task 1: Update Chat Endpoint Logic
**Priority**: High
**Effort**: Medium
**Dependencies**: None

### Description
Update the chat endpoint to handle both new and existing conversations based on conversation_id presence.

### Acceptance Criteria
- If conversation_id is null/invalid, create new Conversation record
- Always return conversation_id in response
- Fetch full message history ordered by created_at
- Build OpenAI-style messages list for agent

### Steps
1. Modify chat endpoint to check for conversation_id
2. Create new Conversation if conversation_id is null
3. Fetch all messages for conversation ordered by created_at
4. Build messages list in OpenAI format (role, content)
5. Ensure conversation_id is always returned in response

### Test Cases
- New conversation creation with null conversation_id
- Existing conversation continuation with valid conversation_id
- Invalid conversation_id triggers new conversation creation

## Task 2: Update Chat Service Layer
**Priority**: High
**Effort**: Medium
**Dependencies**: Task 1

### Description
Enhance the chat service to properly save messages in the correct order and handle conversation management.

### Acceptance Criteria
- User message is saved before agent response
- Agent response is saved with proper metadata
- Conversation history is properly passed to agent
- Agent response includes tool_calls array

### Steps
1. Update process_chat_request to handle conversation creation/history
2. Ensure user message is saved first in database
3. Process agent response with full conversation context
4. Save agent response after user message
5. Return proper response format with conversation_id, response, tool_calls

### Test Cases
- Message persistence order (user first, agent second)
- Conversation history properly passed to agent
- Tool calls correctly returned in response

## Task 3: Enhance Agent Instructions for Error Handling
**Priority**: Medium
**Effort**: Low
**Dependencies**: None

### Description
Update agent instructions to provide better error messages and user-friendly confirmations.

### Acceptance Criteria
- Agent provides friendly confirmations (e.g. "Added task 'Buy groceries' ✅")
- Agent handles errors gracefully (e.g. "Couldn't find that task, sorry!")
- Error messages are clear and non-technical

### Steps
1. Update agent system prompt with error handling instructions
2. Add examples of friendly confirmation messages
3. Include examples of graceful error handling
4. Test agent responses with various error scenarios

### Test Cases
- Successful task operations return friendly confirmations
- Failed operations return user-friendly error messages
- Agent follows consistent response format

## Task 4: Add Logging for Debugging
**Priority**: Medium
**Effort**: Low
**Dependencies**: Task 1, Task 2

### Description
Add logging throughout the conversation management system for debugging purposes.

### Acceptance Criteria
- Log history length before sending to agent
- Log tool calls received from agent
- Log conversation creation/continuation events
- Log error conditions with sufficient detail

### Steps
1. Add logging to chat endpoint for conversation_id handling
2. Add logging to service layer for history length
3. Add logging for tool calls processing
4. Add error logging with context

### Test Cases
- Debug logs show history length correctly
- Tool calls are logged when received from agent
- Error conditions are logged with sufficient context

## Task 5: Create Test Curl Commands
**Priority**: Medium
**Effort**: Low
**Dependencies**: Task 1, Task 2, Task 3

### Description
Generate test curl commands for various conversation scenarios.

### Acceptance Criteria
- Curl command for new conversation creation
- Curl command for continuing existing conversation
- Curl command for error case (invalid task id)
- Expected output documented for each command

### Steps
1. Create curl command for new conversation scenario
2. Create curl command for existing conversation scenario
3. Create curl command for error scenario
4. Document expected output for each test case

### Test Cases
- New conversation curl command works as expected
- Existing conversation curl command works as expected
- Error scenario curl command returns proper error message

## Task 6: Verify Server Restart Persistence
**Priority**: High
**Effort**: Low
**Dependencies**: Task 1, Task 2, Task 3

### Description
Verify that conversation_id remains valid after server restart.

### Acceptance Criteria
- Server restart does not break existing conversation_ids
- Old conversation_ids continue to work after restart
- Conversation history persists across restarts

### Steps
1. Start server and create a conversation
2. Store conversation_id
3. Restart server
4. Continue conversation with stored conversation_id
5. Verify conversation history is preserved

### Test Cases
- Conversation continues successfully after server restart
- Conversation history remains intact after restart
- Stored conversation_id remains valid after restart