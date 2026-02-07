# Implementation Plan: Fix Gemini Native API Integration

## Technical Context

### Current Architecture
The Phase III backend currently uses the OpenAI SDK (`AsyncOpenAI`) to communicate with Google's Gemini AI service. This approach attempts to treat Gemini as an OpenAI-compatible endpoint, which is fundamentally incompatible.

**Current Implementation:**
- File: `phaseIII/backend/app/services/ai_agent.py`
- Uses: `AsyncOpenAI(api_key=config.gemini_api_key, base_url=config.gemini_base_url)`
- Attempts to call: OpenAI-style chat completions endpoint
- Tool definitions: OpenAI function calling format

**Why This Fails:**
- Gemini does not support OpenAI-compatible API endpoints
- The OpenAI SDK sends requests to `/v1/chat/completions` which doesn't exist in Gemini
- Gemini uses a completely different request/response structure
- Gemini's function calling uses `function_declarations` instead of OpenAI's `functions` format

### Backend Technology Stack
- **Framework**: FastAPI (Python)
- **HTTP Client**: Currently none for direct API calls (will add httpx)
- **Authentication**: JWT tokens from Phase II backend
- **Task Operations**: MCP tools for add, delete, update, list, complete
- **Configuration**: Environment variables via Pydantic Settings

### Frontend Integration
- **Framework**: Next.js with TypeScript
- **Backend URL**: `http://127.0.0.1:8003` (Phase III backend)
- **Chat Interface**: Sends user messages to `/api/chat` endpoint
- **No Changes Required**: Frontend remains unchanged

## Current Issues

### 1. 404 API Error
**Error Message:** `"models/gemini-1.5-flash is not found for API version v1main"`

**Root Causes:**
- Using OpenAI SDK with Gemini API (incompatible)
- Wrong API version path (`v1main` instead of `v1beta`)
- Incorrect model name format (`models/gemini-1.5-flash` instead of `gemini-1.5-flash`)
- Wrong endpoint structure (OpenAI format vs Gemini format)

### 2. Request Format Mismatch
**Current:** OpenAI chat completions format
```json
{
  "model": "models/gemini-1.5-flash",
  "messages": [...],
  "functions": [...]
}
```

**Required:** Gemini native format
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "..."}]
    }
  ],
  "tools": [
    {
      "function_declarations": [...]
    }
  ]
}
```

### 3. Response Parsing Incompatibility
**Current:** Expects OpenAI response structure with `choices[0].message.content`

**Required:** Gemini response structure with `candidates[0].content.parts[0].text`

### 4. Tool Calling Format Mismatch
**Current:** OpenAI function calling format

**Required:** Gemini function_declarations format with different schema structure

## Required Changes

### 1. Remove OpenAI SDK Dependency
- Remove `AsyncOpenAI` client initialization
- Remove OpenAI-specific imports
- Add `httpx` for direct HTTP calls

### 2. Implement Native Gemini Client
- Create direct HTTP POST requests to Gemini endpoint
- Use correct endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`
- Pass API key as query parameter: `?key=GEMINI_API_KEY`

### 3. Convert Request Format
- Transform conversation history to Gemini `contents` format
- Convert tool definitions to `function_declarations` format
- Structure requests with `contents` and `tools` fields

### 4. Update Response Parsing
- Parse responses from `candidates[0].content.parts[0].text`
- Handle function calls from Gemini's response structure
- Extract tool call arguments correctly

### 5. Maintain Tool Execution Logic
- Keep existing MCP tool execution unchanged
- Preserve task operation functions (add, delete, update, list, complete)
- Maintain conversation history tracking

## Research Tasks

### 1. Gemini API Request Format
**Endpoint:** `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=API_KEY`

**Request Structure:**
```json
{
  "contents": [
    {
      "role": "user",
      "parts": [
        {"text": "User message here"}
      ]
    },
    {
      "role": "model",
      "parts": [
        {"text": "Assistant response here"}
      ]
    }
  ],
  "tools": [
    {
      "function_declarations": [
        {
          "name": "function_name",
          "description": "Function description",
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
      ]
    }
  ]
}
```

### 2. Gemini Response Format
**Success Response:**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {"text": "Response text here"}
        ],
        "role": "model"
      },
      "finishReason": "STOP"
    }
  ]
}
```

**Function Call Response:**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "functionCall": {
              "name": "function_name",
              "args": {
                "param_name": "value"
              }
            }
          }
        ],
        "role": "model"
      }
    }
  ]
}
```

### 3. Function Declarations Format
Gemini uses `function_declarations` with JSON Schema for parameters:
- `name`: Function name
- `description`: What the function does
- `parameters`: JSON Schema object with `type`, `properties`, `required`

### 4. Conversation History Format
Gemini requires alternating `user` and `model` roles in `contents` array. Each message has `role` and `parts` fields.

## Component Design & API Contracts

### AIAgent Service (`ai_agent.py`)

**Class: AIAgent**

**Constructor:**
```python
def __init__(self):
    self.api_key = config.gemini_api_key
    self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    self.model = "gemini-1.5-flash"
    self.http_client = httpx.AsyncClient()
    self.tools = self._define_tools()
```

**Method: generate_response**
```python
async def generate_response(
    self,
    user_message: str,
    conversation_history: List[Dict],
    user_id: int
) -> str:
    """
    Generate AI response using Gemini native API.

    Args:
        user_message: User's input message
        conversation_history: Previous conversation messages
        user_id: User ID for task operations

    Returns:
        AI-generated response text

    Raises:
        httpx.HTTPError: If API request fails
    """
```

**Method: _convert_to_gemini_format**
```python
def _convert_to_gemini_format(
    self,
    user_message: str,
    conversation_history: List[Dict]
) -> Dict:
    """
    Convert conversation to Gemini contents format.

    Args:
        user_message: Current user message
        conversation_history: Previous messages

    Returns:
        Dictionary with 'contents' and 'tools' fields
    """
```

**Method: _parse_gemini_response**
```python
def _parse_gemini_response(self, response_data: Dict) -> Tuple[str, Optional[Dict]]:
    """
    Parse Gemini API response.

    Args:
        response_data: Raw API response JSON

    Returns:
        Tuple of (response_text, function_call_data)
    """
```

**Method: _execute_tool**
```python
async def _execute_tool(
    self,
    function_name: str,
    arguments: Dict,
    user_id: int
) -> str:
    """
    Execute tool/function call.

    Args:
        function_name: Name of function to execute
        arguments: Function arguments
        user_id: User ID for task operations

    Returns:
        Tool execution result as string
    """
```

**Method: _define_tools**
```python
def _define_tools(self) -> List[Dict]:
    """
    Define available tools in Gemini function_declarations format.

    Returns:
        List of function declarations
    """
```

### API Endpoint Contract

**Endpoint:** `POST /api/chat`

**Request:**
```json
{
  "message": "User message text",
  "conversation_id": "optional-conversation-id"
}
```

**Response:**
```json
{
  "response": "AI response text",
  "conversation_id": "conversation-id"
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

## Implementation Approach

### Phase 1: Setup and Dependencies
1. Add `httpx` to dependencies if not already present
2. Remove OpenAI SDK imports from `ai_agent.py`
3. Update configuration to ensure Gemini API key is available

### Phase 2: Core Client Implementation
1. Replace `AsyncOpenAI` client with `httpx.AsyncClient`
2. Implement `_convert_to_gemini_format` method
3. Implement `_parse_gemini_response` method
4. Update `generate_response` to use native Gemini API

### Phase 3: Tool Calling Conversion
1. Convert tool definitions to `function_declarations` format
2. Update `_define_tools` method with Gemini schema
3. Ensure tool execution logic remains unchanged
4. Test function call parsing from Gemini responses

### Phase 4: Testing and Validation
1. Test basic chat without tool calls
2. Test each task operation: add, delete, update, list, complete
3. Verify conversation history is maintained correctly
4. Confirm no 404 or API key errors occur

## Development Tasks

### Task 1: Remove OpenAI SDK and Add httpx
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Remove `from openai import AsyncOpenAI` import
- Add `import httpx` import
- Replace `self.client = AsyncOpenAI(...)` with `self.http_client = httpx.AsyncClient()`
- Update constructor to store API key and base URL

### Task 2: Implement Gemini Request Conversion
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Create `_convert_to_gemini_format` method
- Convert conversation history to `contents` array
- Ensure alternating user/model roles
- Structure each message with `role` and `parts` fields

### Task 3: Implement Gemini API Call
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Update `generate_response` method
- Build request URL: `{base_url}/models/{model}:generateContent?key={api_key}`
- Send POST request with converted format
- Handle HTTP errors appropriately

### Task 4: Implement Response Parsing
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Create `_parse_gemini_response` method
- Extract text from `candidates[0].content.parts[0].text`
- Detect function calls in response
- Return tuple of (text, function_call_data)

### Task 5: Convert Tool Definitions
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Update `_define_tools` method
- Convert each tool to `function_declarations` format
- Use JSON Schema for parameters
- Include name, description, and parameters for each tool

### Task 6: Handle Function Calls
**File:** `phaseIII/backend/app/services/ai_agent.py`
- Update `generate_response` to detect function calls
- Extract function name and arguments from Gemini response
- Call `_execute_tool` with extracted data
- Send function result back to Gemini for final response

### Task 7: Test All Task Operations
**Testing:**
- Test adding a task: "add a task to buy milk"
- Test viewing tasks: "show my tasks"
- Test deleting a task: "delete the buy milk task"
- Test updating a task: "update buy milk to buy eggs"
- Test completing a task: "mark buy milk as done"
- Verify no 404 errors occur
- Verify responses are contextually appropriate

## Risk Assessment

### High Risk
**Risk:** Breaking existing functionality during refactoring
- **Mitigation:** Make changes incrementally, test after each change
- **Rollback:** Keep backup of original `ai_agent.py` file

**Risk:** Gemini API rate limits or quota issues
- **Mitigation:** Monitor API usage, implement retry logic with exponential backoff
- **Rollback:** None needed, this is operational concern

### Medium Risk
**Risk:** Conversation history format issues causing context loss
- **Mitigation:** Thoroughly test conversation history conversion
- **Validation:** Verify multi-turn conversations maintain context

**Risk:** Function call parsing errors
- **Mitigation:** Add comprehensive error handling for malformed responses
- **Validation:** Test all tool operations multiple times

### Low Risk
**Risk:** Performance degradation from direct HTTP calls
- **Mitigation:** Use async httpx client, maintain connection pooling
- **Validation:** Monitor response times before and after

**Risk:** API key exposure in logs
- **Mitigation:** Ensure API key is passed as query parameter, not logged
- **Validation:** Review logs to confirm no key exposure

## Success Criteria

### Functional Success
- ✅ Zero 404 errors during any chatbot interaction
- ✅ Zero API key validation errors
- ✅ Users can add tasks via natural language
- ✅ Users can delete tasks via natural language
- ✅ Users can view tasks via natural language
- ✅ Users can update tasks via natural language
- ✅ Users can complete tasks via natural language
- ✅ AI responses are relevant and contextually appropriate

### Technical Success
- ✅ No OpenAI SDK dependencies remain
- ✅ All requests use Gemini native REST API
- ✅ Correct endpoint format: `v1beta/models/gemini-1.5-flash:generateContent`
- ✅ Correct request structure with `contents` and `tools`
- ✅ Correct response parsing from `candidates[0].content.parts[0].text`
- ✅ Function calls work correctly with `function_declarations`

### System Integrity
- ✅ No changes to frontend code
- ✅ No changes to authentication system
- ✅ No changes to database schema
- ✅ No changes to task business logic
- ✅ Conversation history continues working
- ✅ All existing endpoints remain functional

### Performance
- ✅ Response times remain under 3 seconds
- ✅ No memory leaks or resource exhaustion
- ✅ HTTP client properly manages connections

## Next Steps

After this plan is approved:
1. Create detailed tasks.md file with specific implementation steps
2. Implement changes following the task list
3. Test each task operation thoroughly
4. Validate all success criteria are met
5. Document any issues or edge cases discovered during implementation
