# Todo AI Chatbot - AI Integration Specification (Step 5)

## 1. Constitution Reinforcement

**Core Isolation Principles:**
- Phase III must remain **completely isolated** from Phase II — no modifications, overwrites, refactors, or direct imports from Phase II folders/code.
- Phase II frontend & backend are **READ-ONLY** forever.
- Phase III lives in separate top-level folders (e.g., `phase3-backend/`, `phase3-frontend/`, `specs/`, etc.).
- No manual coding — all implementation generated via Claude Code from specs/plans/tasks.

**Step 5-Specific Rules:**
- The AI integration **MUST create a standalone agent** with MCP tools connection for testing.
- **Stateless Design**: Agent receives conversation history each time it's invoked.
- **MCP Tool Execution**: Agent executes tools via MCP server with configurable URL.
- **Tool Mapping**: Natural language mapped to specific MCP tools (add_task, list_tasks, complete_task, delete_task, update_task).
- **Response Generation**: Agent generates natural language responses based on tool executions.
- **Error Handling**: Graceful handling of MCP server unavailability, tool execution failures.
- **All database operations** must remain **async** using SQLModel `AsyncSession`.

## 2. Step 5 Overview & Goals

**Primary Objectives:**
- Create a standalone OpenAI Agent with MCP tools integration.
- Connect to MCP tools server via configurable URL for task operations.
- Prepare agent for integration with chat endpoint in Step 6.
- Maintain stateless design while providing rich AI interactions.
- Implement proper error handling for AI and MCP service failures.

**Expected Outcomes:**
- Standalone agent that can process conversation history and execute MCP tools.
- Natural language properly mapped to appropriate MCP tool calls.
- Tool execution results incorporated into AI responses.
- Robust error handling for service failures.
- Test runner script for manual testing of agent functionality.

## 3. Dependencies & Prerequisites

- Step 4: Chat endpoint with authentication and message persistence.
- Step 3: MCP server with all 5 tools registered.
- Step 2: MCP tools implementation for database operations.
- Step 1: Database models and async session utilities.
- Installed packages: `openai-agents`, `mcp-use`, `fastapi`, `uvicorn`, `pydantic`, `sqlmodel`.
- `.env` with: `OPENAI_API_KEY`, `MCP_SERVER_URL`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`.

## 4. AI Integration Specification

### OpenAI Agent Configuration
- **Package**: openai-agents (pip install openai-agents)
- **Model**: gpt-4o or gpt-4o-mini (latest available model)
- **Instructions**: Detailed instructions for the agent on how to interpret user requests and use MCP tools appropriately
- **Temperature**: 0.7 for balanced creativity and accuracy
- **Max Tokens**: Appropriate limit for response generation

### MCP Client Integration
- **Server URL**: Configurable via MCP_SERVER_URL environment variable
- **Transport**: Prefer streamable-http/sse communication with MCP server
- **Timeout**: 30 seconds for tool execution
- **Retry Policy**: Up to 3 retries on network failures
- **Connection Pool**: Managed connection pool for efficiency

### Agent Behavior Specification
- **Task Creation**: When user mentions adding/creating/remembering something, use add_task tool
- **Task Listing**: When user asks to see/show/list tasks, use list_tasks with appropriate filter
- **Task Completion**: When user says done/complete/finished, use complete_task
- **Task Deletion**: When user says delete/remove/cancel, use delete_task
- **Task Update**: When user says change/update/rename, use update_task
- **Confirmation**: Always provide friendly confirmation after tool execution
- **Error Handling**: Gracefully handle task not found and other errors with helpful messages

### Agent Initialization
1. Initialize OpenAI Agent with MCP tools client
2. Configure with detailed instructions for task management
3. Set up proper tool definitions for MCP integration
4. Prepare for conversation history input

### Error Handling Specification
- **MCP Server Unavailable**: Return graceful error message to user
- **Tool Execution Failure**: Return helpful error message to user
- **AI Service Unavailable**: Return graceful error message to user
- **Authentication Errors**: Handle gracefully for tool access
- **Validation Errors**: Return specific validation error messages
- **Database Errors**: Return appropriate error messages when database unavailable

### Security Requirements
- **Token Security**: OpenAI API key stored securely in environment variables
- **Rate Limiting**: Respect OpenAI API rate limits
- **Input Sanitization**: All user inputs sanitized before passing to AI
- **MCP Server Security**: Secure communication with MCP server

### Performance Requirements
- **Response Time**: Aim for responses within 5-10 seconds under normal load
- **Concurrent Sessions**: Support multiple concurrent AI sessions
- **Efficient Tool Calls**: Minimize unnecessary tool executions

### Testing Requirements
- **Standalone Test Script**: Create test_agent.py for manual testing
- **Tool Call Verification**: Verify agent correctly maps language to tools
- **Response Quality**: Ensure responses incorporate tool results appropriately
- **Error Scenario Testing**: Test error handling for various failure modes