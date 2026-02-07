# Todo AI Chatbot - AI Integration Implementation Plan (Step 5)

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
- Installed packages: `openai-agents`, `fastapi`, `uvicorn`, `pydantic`, `sqlmodel`.
- `.env` with: `OPENAI_API_KEY`, `MCP_SERVER_URL`, `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`.

## 4. Detailed Task Breakdown

### Task 5.1: Update Requirements with Correct Package
- **Description**: Update the requirements file to include the correct OpenAI Agents package
- **Inputs needed**: Current requirements.txt, correct package name (openai-agents)
- **Outputs/Files to generate**:
  - `phase3-backend/requirements.txt` (updated with openai-agents package)
- **Dependencies**: None (can be done independently)
- **Estimated complexity**: Low
- **Claude prompt hint**: "Update requirements.txt with openai-agents package instead of openai."

### Task 5.2: Create Standalone Agent Module
- **Description**: Create the standalone agent implementation that connects to MCP tools
- **Inputs needed**: OpenAI API configuration, MCP server URL from environment variables
- **Outputs/Files to generate**:
  - `phase3-backend/app/agent/todo_agent.py` (standalone agent implementation)
- **Dependencies**: None (can be done independently)
- **Estimated complexity**: High
- **Claude prompt hint**: "Create standalone OpenAI agent that connects to MCP tools server with proper instructions for task management. Use gpt-4o or gpt-4o-mini model, attach MCP via SDK client with configurable MCP_SERVER_URL env var, prefer streamable-http transport."

### Task 5.3: Create Agent Configuration
- **Description**: Set up configuration for the standalone agent
- **Inputs needed**: Agent configuration parameters from environment variables
- **Outputs/Files to generate**:
  - `phase3-backend/app/agent/config.py` (agent configuration)
- **Dependencies**: None (can be done independently)
- **Estimated complexity**: Low
- **Claude prompt hint**: "Create configuration module for standalone agent with environment variable loading."

### Task 5.4: Create Agent Service Wrapper
- **Description**: Create a service wrapper for the agent to process conversation history
- **Inputs needed**: Standalone agent implementation, configuration
- **Outputs/Files to generate**:
  - `phase3-backend/app/agent/service.py` (agent service wrapper)
- **Dependencies**: Tasks 5.2, 5.3
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create agent service wrapper that takes conversation history and processes it with the agent."

### Task 5.5: Create Test Runner Script
- **Description**: Create a standalone test script for manual testing of the agent
- **Inputs needed**: Agent implementation, service wrapper
- **Outputs/Files to generate**:
  - `phase3-backend/test_agent.py` (test runner script)
- **Dependencies**: Tasks 5.2-5.4
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create standalone test runner script for the agent with example conversation flows."

### Task 5.6: Create Agent Integration Tests
- **Description**: Develop comprehensive tests for the agent functionality
- **Inputs needed**: Complete agent implementation
- **Outputs/Files to generate**:
  - `phase3-backend/tests/test_agent_integration.py` (tests for agent functionality)
- **Dependencies**: Tasks 5.1-5.5
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create comprehensive tests for the standalone agent covering tool mapping and response generation."

## 5. Risks & Mitigations

### Risk 1: Package Availability
- **Issue**: The `openai-agents` package may not exist or be different from expected
- **Mitigation**: Verify the actual package name and API before implementation, use the official OpenAI SDK if needed.

### Risk 2: MCP Server Connection
- **Issue**: MCP server may be unavailable or have connection issues during testing
- **Mitigation**: Implement proper error handling and fallback mechanisms, include mocking capabilities for tests.

### Risk 3: Agent Behavior Accuracy
- **Issue**: Agent may not correctly map natural language to appropriate tools
- **Mitigation**: Include detailed instructions and examples in the agent configuration, implement thorough testing.

### Risk 4: Performance Issues
- **Issue**: Agent responses may be slow or resource-intensive
- **Mitigation**: Optimize agent instructions, implement efficient tool usage patterns, monitor performance during testing.

### Risk 5: Error Handling Complexity
- **Issue**: Multiple service dependencies (OpenAI, MCP) increase error handling complexity
- **Mitigation**: Implement comprehensive error handling with clear error messages and graceful degradation.

### Risk 6: MCP Transport Incompatibility
- **Issue**: Streamable-http transport may not be compatible with the MCP server
- **Mitigation**: Test with streamable-http first, fallback to sse if needed.

## 6. Success Criteria for Step 5
- Standalone agent successfully connects to MCP tools server
- Natural language properly mapped to appropriate MCP tool calls
- Tool execution results incorporated into AI responses
- Error handling works for AI and MCP service failures
- Test runner script allows manual testing of agent functionality
- Tests pass for all agent functionality
- Agent maintains stateless design and proper conversation history processing
- Agent correctly calls tools in standalone test_runner.py with sample messages like 'Add task buy groceries'
- Ready for Step 6 integration with chat endpoint

## 7. Next Actions
- Immediate next: Implement Task 5.1 (update requirements) to use correct package
- Suggest prompt for first implementation task: "Based on this plan and previous spec, generate the code for Task 5.1: update requirements.txt with openai-agents package instead of openai in phase3-backend/requirements.txt. Include openai-agents and any other necessary packages."
- After all tasks: Review full standalone agent implementation, then move to Step 6 spec/plan (Chat Endpoint Integration)