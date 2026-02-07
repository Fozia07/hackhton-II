# Implementation Tasks: Fix Gemini Native API Integration

## Overview
This document contains actionable, testable tasks for implementing the Gemini native API integration. Tasks are ordered by dependency and should be completed sequentially.

## Task Status Legend
- ⏳ Pending
- 🔄 In Progress
- ✅ Completed
- ❌ Blocked

---

## Task 1: Setup Dependencies and Remove OpenAI SDK
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** None

### Description
Remove OpenAI SDK dependency and ensure httpx is available for direct HTTP calls to Gemini API.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`
- `phaseIII/backend/requirements.txt` (if httpx not present)

### Implementation Steps
1. Check if `httpx` is in requirements.txt, add if missing
2. Remove `from openai import AsyncOpenAI` import from ai_agent.py
3. Add `import httpx` import to ai_agent.py
4. Remove any other OpenAI-specific imports

### Acceptance Criteria
- [ ] No OpenAI imports remain in ai_agent.py
- [ ] httpx is imported successfully
- [ ] File has no import errors when loaded
- [ ] No references to `AsyncOpenAI` class remain

### Test Cases
```python
# Verify imports work
import sys
sys.path.insert(0, 'phaseIII/backend')
from app.services.ai_agent import AIAgent
# Should not raise ImportError
```

---

## Task 2: Update AIAgent Constructor
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 1

### Description
Replace OpenAI client initialization with httpx client and store Gemini API configuration.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. Locate `__init__` method in AIAgent class
2. Remove `self.client = AsyncOpenAI(...)` line
3. Add `self.http_client = httpx.AsyncClient(timeout=30.0)`
4. Store API configuration:
   ```python
   self.api_key = config.gemini_api_key
   self.base_url = "https://generativelanguage.googleapis.com/v1beta"
   self.model = "gemini-1.5-flash"
   ```
5. Keep existing tool definitions and other initialization

### Acceptance Criteria
- [ ] No AsyncOpenAI client initialization
- [ ] httpx.AsyncClient is created with appropriate timeout
- [ ] API key is stored from config
- [ ] Base URL points to Gemini v1beta endpoint
- [ ] Model name is "gemini-1.5-flash" (without "models/" prefix)
- [ ] Constructor completes without errors

### Test Cases
```python
# Test constructor
agent = AIAgent()
assert hasattr(agent, 'http_client')
assert agent.model == "gemini-1.5-flash"
assert "v1beta" in agent.base_url
assert agent.api_key is not None
```

---

## Task 3: Implement Tool Definitions Converter
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Medium
**Dependencies:** Task 2

### Description
Convert existing tool definitions from OpenAI format to Gemini function_declarations format.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. Locate or create `_define_tools` method
2. Convert each tool to Gemini format:
   ```python
   {
     "name": "tool_name",
     "description": "Tool description",
     "parameters": {
       "type": "object",
       "properties": {
         "param_name": {
           "type": "string",
           "description": "Parameter description"
         }
       },
       "required": ["param_name"]
     }
   }
   ```
3. Ensure all 5 task operations are defined:
   - add_task
   - delete_task
   - update_task
   - list_tasks
   - complete_task

### Acceptance Criteria
- [ ] Method returns list of function declarations
- [ ] Each tool has name, description, and parameters
- [ ] Parameters follow JSON Schema format
- [ ] All 5 task operations are defined
- [ ] Required parameters are specified correctly
- [ ] No OpenAI-specific format remains

### Test Cases
```python
# Test tool definitions
agent = AIAgent()
tools = agent._define_tools()
assert len(tools) == 5
assert all('name' in tool for tool in tools)
assert all('description' in tool for tool in tools)
assert all('parameters' in tool for tool in tools)
tool_names = [t['name'] for t in tools]
assert 'add_task' in tool_names
assert 'delete_task' in tool_names
```

---

## Task 4: Implement Conversation Format Converter
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Medium
**Dependencies:** Task 3

### Description
Create method to convert conversation history and current message to Gemini contents format.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. Create `_convert_to_gemini_format` method
2. Accept parameters: `user_message: str`, `conversation_history: List[Dict]`
3. Build contents array with alternating user/model roles:
   ```python
   contents = []
   for msg in conversation_history:
       role = "user" if msg["role"] == "user" else "model"
       contents.append({
           "role": role,
           "parts": [{"text": msg["content"]}]
       })
   # Add current user message
   contents.append({
       "role": "user",
       "parts": [{"text": user_message}]
   })
   ```
4. Return dictionary with contents and tools:
   ```python
   return {
       "contents": contents,
       "tools": [{"function_declarations": self._define_tools()}]
   }
   ```

### Acceptance Criteria
- [ ] Method accepts user_message and conversation_history
- [ ] Returns dictionary with 'contents' and 'tools' keys
- [ ] Contents array has correct role/parts structure
- [ ] Roles alternate between user and model
- [ ] Current user message is appended last
- [ ] Tools are included in correct format

### Test Cases
```python
# Test conversion
agent = AIAgent()
history = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there"}
]
result = agent._convert_to_gemini_format("How are you?", history)
assert "contents" in result
assert "tools" in result
assert len(result["contents"]) == 3
assert result["contents"][-1]["role"] == "user"
assert result["contents"][-1]["parts"][0]["text"] == "How are you?"
```

---

## Task 5: Implement Gemini Response Parser
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Medium
**Dependencies:** Task 4

### Description
Create method to parse Gemini API responses and extract text or function calls.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. Create `_parse_gemini_response` method
2. Accept parameter: `response_data: Dict`
3. Extract text response:
   ```python
   text = response_data["candidates"][0]["content"]["parts"][0].get("text")
   ```
4. Check for function calls:
   ```python
   function_call = response_data["candidates"][0]["content"]["parts"][0].get("functionCall")
   ```
5. Return tuple: `(text, function_call)`
6. Add error handling for missing keys

### Acceptance Criteria
- [ ] Method accepts response_data dictionary
- [ ] Returns tuple of (text, function_call)
- [ ] Correctly extracts text from candidates[0].content.parts[0].text
- [ ] Correctly extracts function calls when present
- [ ] Returns (None, function_call) when function call exists
- [ ] Returns (text, None) when only text exists
- [ ] Handles missing keys gracefully

### Test Cases
```python
# Test text response parsing
agent = AIAgent()
response = {
    "candidates": [{
        "content": {
            "parts": [{"text": "Hello!"}],
            "role": "model"
        }
    }]
}
text, func = agent._parse_gemini_response(response)
assert text == "Hello!"
assert func is None

# Test function call parsing
response_with_func = {
    "candidates": [{
        "content": {
            "parts": [{
                "functionCall": {
                    "name": "add_task",
                    "args": {"title": "Buy milk"}
                }
            }],
            "role": "model"
        }
    }]
}
text, func = agent._parse_gemini_response(response_with_func)
assert func is not None
assert func["name"] == "add_task"
```

---

## Task 6: Implement Gemini API Request Handler
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** High
**Dependencies:** Task 5

### Description
Update generate_response method to make direct HTTP calls to Gemini native API.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. Locate `generate_response` method
2. Build request URL:
   ```python
   url = f"{self.base_url}/models/{self.model}:generateContent"
   params = {"key": self.api_key}
   ```
3. Convert conversation to Gemini format:
   ```python
   request_body = self._convert_to_gemini_format(user_message, conversation_history)
   ```
4. Make HTTP POST request:
   ```python
   response = await self.http_client.post(url, params=params, json=request_body)
   response.raise_for_status()
   response_data = response.json()
   ```
5. Parse response:
   ```python
   text, function_call = self._parse_gemini_response(response_data)
   ```
6. Handle function calls if present:
   ```python
   if function_call:
       tool_result = await self._execute_tool(
           function_call["name"],
           function_call["args"],
           user_id
       )
       # Make second API call with tool result
       # Return final response
   ```
7. Return text response
8. Add comprehensive error handling

### Acceptance Criteria
- [ ] Method makes POST request to correct Gemini endpoint
- [ ] API key is passed as query parameter
- [ ] Request body uses Gemini format
- [ ] Response is parsed correctly
- [ ] Function calls are detected and executed
- [ ] Tool results are sent back to Gemini for final response
- [ ] Text response is returned to caller
- [ ] HTTP errors are caught and handled
- [ ] Method signature remains compatible with existing code

### Test Cases
```python
# Integration test (requires valid API key)
agent = AIAgent()
response = await agent.generate_response(
    user_message="Hello",
    conversation_history=[],
    user_id=1
)
assert isinstance(response, str)
assert len(response) > 0
```

---

## Task 7: Handle Function Call Round-Trip
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** High
**Dependencies:** Task 6

### Description
Implement complete function calling flow: detect function call, execute tool, send result back to Gemini, return final response.

### Files to Modify
- `phaseIII/backend/app/services/ai_agent.py`

### Implementation Steps
1. In `generate_response`, after detecting function call:
2. Execute the tool:
   ```python
   tool_result = await self._execute_tool(
       function_call["name"],
       function_call["args"],
       user_id
   )
   ```
3. Build second request with tool result:
   ```python
   # Add function call to conversation
   contents.append({
       "role": "model",
       "parts": [{"functionCall": function_call}]
   })
   # Add function response
   contents.append({
       "role": "function",
       "parts": [{
           "functionResponse": {
               "name": function_call["name"],
               "response": {"result": tool_result}
           }
       }]
   })
   ```
4. Make second API call with updated contents
5. Parse and return final response

### Acceptance Criteria
- [ ] Function calls are detected correctly
- [ ] Tools are executed with correct arguments
- [ ] Tool results are formatted correctly
- [ ] Second API call includes function call and response
- [ ] Final response is natural language, not raw tool output
- [ ] Multi-turn function calling works if needed
- [ ] Errors in tool execution are handled gracefully

### Test Cases
```python
# Test add task flow
agent = AIAgent()
response = await agent.generate_response(
    user_message="add a task to buy milk",
    conversation_history=[],
    user_id=1
)
assert "buy milk" in response.lower() or "added" in response.lower()

# Test list tasks flow
response = await agent.generate_response(
    user_message="show my tasks",
    conversation_history=[],
    user_id=1
)
assert isinstance(response, str)
```

---

## Task 8: Test Task Addition via Chatbot
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 7

### Description
Verify users can successfully add tasks through natural language commands.

### Test Scenarios
1. Simple task addition: "add a task to buy milk"
2. Task with details: "add a task to call dentist tomorrow"
3. Multiple tasks in sequence

### Acceptance Criteria
- [ ] No 404 errors occur
- [ ] No API key errors occur
- [ ] Task is created in database
- [ ] Chatbot confirms task creation
- [ ] Response includes task name
- [ ] Response is natural and helpful

### Manual Test Steps
1. Start Phase III backend on port 8003
2. Open frontend at http://localhost:3000
3. Login as test user (hamzah12)
4. Type: "add a task to buy milk"
5. Verify response confirms task creation
6. Check backend logs for no errors
7. Verify task appears in database

---

## Task 9: Test Task Viewing via Chatbot
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 8

### Description
Verify users can successfully view their tasks through natural language queries.

### Test Scenarios
1. View all tasks: "show my tasks"
2. View tasks: "what are my tasks?"
3. View tasks: "list all my todos"

### Acceptance Criteria
- [ ] No 404 errors occur
- [ ] All user's tasks are retrieved
- [ ] Tasks are displayed in readable format
- [ ] Response includes task titles and status
- [ ] Empty list is handled gracefully

### Manual Test Steps
1. Ensure test user has some tasks
2. Type: "show my tasks"
3. Verify all tasks are listed
4. Verify format is clear and readable
5. Check backend logs for no errors

---

## Task 10: Test Task Deletion via Chatbot
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 9

### Description
Verify users can successfully delete tasks through natural language commands.

### Test Scenarios
1. Delete by name: "delete the buy milk task"
2. Delete by description: "remove buy milk"
3. Delete non-existent task (error handling)

### Acceptance Criteria
- [ ] No 404 errors occur
- [ ] Task is deleted from database
- [ ] Chatbot confirms deletion
- [ ] Response includes deleted task name
- [ ] Non-existent task deletion is handled gracefully

### Manual Test Steps
1. Add a test task: "add a task to buy milk"
2. Delete it: "delete the buy milk task"
3. Verify response confirms deletion
4. Try to view tasks, verify it's gone
5. Check backend logs for no errors

---

## Task 11: Test Task Updates via Chatbot
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 10

### Description
Verify users can successfully update tasks through natural language commands.

### Test Scenarios
1. Update task title: "update buy milk to buy eggs"
2. Update task details: "change buy milk task to buy bread"
3. Update non-existent task (error handling)

### Acceptance Criteria
- [ ] No 404 errors occur
- [ ] Task is updated in database
- [ ] Chatbot confirms update
- [ ] Response includes old and new task names
- [ ] Non-existent task update is handled gracefully

### Manual Test Steps
1. Add a test task: "add a task to buy milk"
2. Update it: "update buy milk to buy eggs"
3. Verify response confirms update
4. View tasks to verify change
5. Check backend logs for no errors

---

## Task 12: Test Task Completion via Chatbot
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 11

### Description
Verify users can successfully mark tasks as complete through natural language commands.

### Test Scenarios
1. Complete task: "mark buy milk as done"
2. Complete task: "complete the buy milk task"
3. Complete already completed task (idempotency)

### Acceptance Criteria
- [ ] No 404 errors occur
- [ ] Task status is updated to completed
- [ ] Chatbot confirms completion
- [ ] Response includes completed task name
- [ ] Already completed task is handled gracefully

### Manual Test Steps
1. Add a test task: "add a task to buy milk"
2. Complete it: "mark buy milk as done"
3. Verify response confirms completion
4. View tasks to verify status change
5. Try completing again, verify graceful handling
6. Check backend logs for no errors

---

## Task 13: Verify System Integrity
**Status:** ⏳ Pending
**Priority:** High
**Estimated Complexity:** Low
**Dependencies:** Task 12

### Description
Verify all existing functionality continues to work correctly after changes.

### Test Areas
1. User authentication and login
2. Conversation history persistence
3. Database operations
4. Frontend interface behavior
5. Other API endpoints

### Acceptance Criteria
- [ ] Users can login successfully
- [ ] JWT tokens work correctly
- [ ] Conversation history is maintained across messages
- [ ] Database queries execute without errors
- [ ] Frontend displays responses correctly
- [ ] No regression in existing features

### Manual Test Steps
1. Test login flow
2. Send multiple chat messages, verify history
3. Logout and login again, verify session
4. Check database for data integrity
5. Test other API endpoints if any
6. Monitor backend logs for unexpected errors

---

## Task 14: Performance and Error Handling Validation
**Status:** ⏳ Pending
**Priority:** Medium
**Estimated Complexity:** Low
**Dependencies:** Task 13

### Description
Verify system meets performance requirements and handles errors gracefully.

### Test Scenarios
1. Response time under normal load
2. Invalid API key handling
3. Network timeout handling
4. Malformed request handling
5. Rate limit handling

### Acceptance Criteria
- [ ] AI responses generated within 3 seconds
- [ ] Invalid API key returns clear error message
- [ ] Network timeouts are caught and reported
- [ ] Malformed requests don't crash server
- [ ] Rate limits are handled with retry logic
- [ ] All errors are logged appropriately

### Manual Test Steps
1. Measure response times for 10 requests
2. Temporarily use invalid API key, verify error
3. Simulate network issues, verify handling
4. Send malformed requests, verify graceful failure
5. Review error logs for completeness

---

## Summary

### Total Tasks: 14
- Setup and Infrastructure: 2 tasks
- Core Implementation: 5 tasks
- Testing: 7 tasks

### Critical Path
Task 1 → Task 2 → Task 3 → Task 4 → Task 5 → Task 6 → Task 7 → Task 8 → Task 9 → Task 10 → Task 11 → Task 12 → Task 13 → Task 14

### Estimated Timeline
- Setup: 30 minutes
- Core Implementation: 3-4 hours
- Testing: 2-3 hours
- **Total: 6-8 hours**

### Risk Mitigation
- Test after each task completion
- Keep backup of original ai_agent.py
- Monitor backend logs continuously
- Verify no 404 errors at each step

### Success Metrics
- Zero 404 errors
- Zero API key errors
- All 5 task operations working
- Response times under 3 seconds
- No regression in existing features
