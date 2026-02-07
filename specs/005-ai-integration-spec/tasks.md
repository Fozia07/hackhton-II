# Todo AI Chatbot - AI Integration Implementation Tasks (Step 5)

## Task 5.1: Update Requirements with Correct Package

**Description**: Update the requirements file to include the correct OpenAI Agents package

**Status**: Pending

**Dependencies**: None (can be done independently)

**Inputs**: Current requirements.txt, correct package name (openai-agents)

**Outputs**:
- `phase3-backend/requirements.txt` (updated with openai-agents package)

**Complexity**: Low

**Acceptance Criteria**:
- [ ] `requirements.txt` updated with openai-agents package
- [ ] Old openai package reference removed or updated as appropriate
- [ ] All existing dependencies preserved
- [ ] Package versions compatible with existing codebase
- [ ] mcp-use package removed from requirements

**Next Action**: Execute Claude prompt to update requirements.txt with openai-agents package

---

## Task 5.2: Create Standalone Agent Module

**Description**: Create the standalone agent implementation that connects to MCP tools

**Status**: Pending

**Dependencies**: None (can be done independently)

**Inputs**: OpenAI API configuration, MCP server URL from environment variables

**Outputs**:
- `phase3-backend/app/agent/todo_agent.py` (standalone agent implementation)

**Complexity**: High

**Acceptance Criteria**:
- [ ] `todo_agent.py` created with standalone agent implementation
- [ ] Agent properly configured with MCP tools connection
- [ ] Uses gpt-4o or gpt-4o-mini model as specified
- [ ] MCP attached via SDK client with configurable MCP_SERVER_URL env var
- [ ] Prefers streamable-http transport as specified
- [ ] Natural language properly mapped to appropriate tools
- [ ] Error handling for OpenAI and MCP service failures
- [ ] Conversation history properly handled for context
- [ ] Tool execution results incorporated into responses

**Next Action**: Execute Claude prompt to create standalone agent module

---

## Task 5.3: Create Agent Configuration

**Description**: Set up configuration for the standalone agent

**Status**: Pending

**Dependencies**: None (can be done independently)

**Inputs**: Agent configuration parameters from environment variables

**Outputs**:
- `phase3-backend/app/agent/config.py` (agent configuration)

**Complexity**: Low

**Acceptance Criteria**:
- [ ] `config.py` created with agent configuration
- [ ] Environment variable loading for sensitive data
- [ ] Default values for optional settings
- [ ] Configuration validation implemented
- [ ] MCP server URL loaded from environment variable

**Next Action**: Execute Claude prompt to create agent configuration

---

## Task 5.4: Create Agent Service Wrapper

**Description**: Create a service wrapper for the agent to process conversation history

**Status**: Pending

**Dependencies**: Tasks 5.2, 5.3

**Inputs**: Standalone agent implementation, configuration

**Outputs**:
- `phase3-backend/app/agent/service.py` (agent service wrapper)

**Complexity**: Medium

**Acceptance Criteria**:
- [ ] `service.py` created with agent service wrapper
- [ ] Function to process conversation history with agent
- [ ] Proper error handling for agent service failures
- [ ] Input sanitization implemented
- [ ] Async compatibility for integration with FastAPI
- [ ] Conversation history properly formatted for agent consumption

**Next Action**: Execute Claude prompt to create agent service wrapper

---

## Task 5.5: Create Test Runner Script

**Description**: Create a standalone test script for manual testing of the agent

**Status**: Pending

**Dependencies**: Tasks 5.2-5.4

**Inputs**: Agent implementation, service wrapper

**Outputs**:
- `phase3-backend/test_agent.py` (test runner script)

**Complexity**: Medium

**Acceptance Criteria**:
- [ ] `test_agent.py` created with test runner functionality
- [ ] Interactive mode for manual testing
- [ ] Example conversation flows included
- [ ] Error handling for test scenarios
- [ ] Clear instructions for running tests
- [ ] Sample messages like 'Add task buy groceries' included

**Next Action**: Execute Claude prompt to create test runner script

---

## Task 5.6: Create Agent Integration Tests

**Description**: Develop comprehensive tests for the agent functionality

**Status**: Pending

**Dependencies**: Tasks 5.1-5.5

**Inputs**: Complete agent implementation

**Outputs**:
- `phase3-backend/tests/test_agent_integration.py` (tests for agent functionality)

**Complexity**: Medium

**Acceptance Criteria**:
- [ ] `test_agent_integration.py` created with comprehensive tests
- [ ] Tests for agent behavior and tool mapping
- [ ] Tests for response generation
- [ ] Tests for error handling scenarios
- [ ] Mock implementations for external services
- [ ] All tests pass successfully
- [ ] Tests verify agent correctly calls tools with sample messages

**Next Action**: Execute Claude prompt to create agent integration tests