# Todo AI Chatbot - Chat Agent Integration Specification (Step 6)

## 1. Constitution Reinforcement

**Core Isolation Principles:**
- Phase III must remain **completely isolated** from Phase II — no modifications, overwrites, refactors, or direct imports from Phase II folders/code.
- Phase II frontend & backend are **READ-ONLY** forever.
- Phase III lives in separate top-level folders (e.g., `phase3-backend/`, `phase3-frontend/`, `specs/`, etc.).
- No manual coding — all implementation generated via Claude Code from specs/plans/tasks.

**Step 6-Specific Rules:**
- The chat endpoint **MUST integrate** with the standalone agent created in Step 5.
- **Stateless Design**: Conversation history fetched from database and passed to agent on each request.
- **MCP Tool Execution**: Agent executes tools via MCP server using conversation context.
- **Natural Language Processing**: User messages properly interpreted and mapped to appropriate tools.
- **Response Generation**: Agent generates natural language responses based on tool execution results.
- **Error Handling**: Graceful handling of agent service failures, MCP server unavailability.
- **All database operations** must remain **async** using SQLModel `AsyncSession`.

## 2. Step 6 Overview & Goals

**Primary Objectives:**
- Integrate the standalone agent from Step 5 with the existing chat endpoint.
- Connect conversation history from database to agent for context awareness.
- Enable real AI-powered task management through natural language.
- Maintain stateless design while providing rich AI interactions.
- Implement proper error handling for AI and MCP service failures.

**Expected Outcomes:**
- Chat endpoint returns real AI-generated responses based on tool executions.
- Natural language properly mapped to appropriate MCP tool calls.
- Conversation history properly provided to agent for context.
- Tool execution results incorporated into AI responses.
- Robust error handling for service failures.

## 3. Dependencies & Prerequisites

- Step 5: Standalone agent with MCP tools integration (completed).
- Step 4: Chat endpoint with authentication and message persistence.
- Step 3: MCP server running with all 5 tools registered.
- Step 2: MCP tools implementation for database operations.
- Step 1: Database models and async session utilities.
- Installed packages: `google-generativeai`, `mcp-use`, `fastapi`, `uvicorn`, `pydantic`, `sqlmodel`.
- `.env` with: `GEMINI_API_KEY`, `MCP_SERVER_URL`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`.

## 4. Chat Agent Integration Specification

### Agent Integration Points
- **Service Layer**: Update `process_chat_request` in chat service to use the agent from Step 5
- **Conversation History**: Fetch conversation history from database and provide to agent
- **Message Persistence**: Store user and assistant messages in database with proper roles
- **Response Handling**: Process agent's response for return to client
- **Agent Service Call**: Use generic `agent_runner.process(messages: List[Dict[str, str]], user_id: str)` where messages is the full OpenAI-style history including new user message
- **Async Processing**: Endpoint remains async; await agent processing

### Agent Configuration
- **API Key**: GEMINI_API_KEY from environment variables
- **Model**: gemini-pro or gemini-1.5-pro (from Step 5 configuration)
- **Instructions**: Updated instructions for the agent on how to interpret user requests and use MCP tools appropriately
- **Tools**: Reference to MCP server tools via MCP client (from Step 5)
- **Temperature**: 0.7 for balanced creativity and accuracy (configured in Step 5)
- **Max Tokens**: Appropriate limit for response generation (configured in Step 5)

### Agent Behavior Specification
- **Task Creation**: When user mentions adding/creating/remembering something, use add_task tool
- **Task Listing**: When user asks to see/show/list tasks, use list_tasks with appropriate filter
- **Task Completion**: When user says done/complete/finished, use complete_task
- **Task Deletion**: When user says delete/remove/cancel, use delete_task
- **Task Update**: When user says change/update/rename, use update_task
- **Confirmation**: Always provide friendly confirmation after tool execution
- **Error Handling**: Gracefully handle task not found and other errors with helpful messages

### Conversation Flow with Agent Integration
1. Receive user message from request at `/api/{user_id}/chat`
2. Authenticate user via JWT and validate user_id
3. Fetch conversation history from database using conversation_id (or create new if not provided)
4. Build message array for agent (existing history + new user message) with proper roles
5. Store user message in database with proper role ('user')
6. **NEW**: Pass full message history to agent_runner.process() from Step 5 using async/await
7. **NEW**: Agent executes appropriate MCP tool(s) via MCP server
8. **NEW**: Agent returns (response_text, tool_calls_list) → capture both values
9. **NEW**: Save response_text as assistant message to database and return both response_text and tool_calls in response
10. Store assistant response in database with proper role ('assistant')
11. Return response to client with conversation_id, response_text, and tool_calls array (even if empty)

### Error Handling Specification
- **Agent Service Unavailable**: Return graceful error message to user
- **Tool Execution Failure**: Return helpful error message to user
- **AI Service Unavailable**: Return graceful error message to user
- **Authentication Errors**: Continue to return 401 with clear error message
- **Validation Errors**: Continue to return 400 with specific validation error
- **Database Errors**: Continue to return 500 with error message when database unavailable

### Security Requirements
- **Token Security**: OpenAI API key stored securely in environment variables
- **Rate Limiting**: Respect OpenAI API rate limits
- **Input Sanitization**: All user inputs sanitized before passing to AI
- **MCP Server Security**: Secure communication with MCP server

### Performance Requirements
- **Response Time**: Aim for responses within 5-10 seconds under normal load
- **Concurrent Sessions**: Support multiple concurrent AI sessions
- **Efficient Tool Calls**: Minimize unnecessary tool executions