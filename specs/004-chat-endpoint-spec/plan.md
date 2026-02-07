# Todo AI Chatbot - Chat Endpoint Implementation Plan

## 1. Constitution Reinforcement

**Core Isolation Principles:**
- Phase III must remain **completely isolated** from Phase II — no modifications, overwrites, refactors, or direct imports from Phase II folders/code.
- Phase II frontend & backend are **READ-ONLY** forever.
- Phase III lives in separate top-level folders (e.g., `phaseIII/backend/`, `phaseIII/frontend/`, `specs/`, etc.).
- No manual coding — all implementation generated via Claude Code from specs/plans/tasks.

**Step 4-Specific Rules:**
- The chat endpoint **MUST be completely stateless** — all state (conversations, messages) fetched and stored in Neon PostgreSQL via SQLModel on every request.
- Use **JWT token authentication** reused from Phase II logic (OAuth2PasswordBearer scheme, python-jose + passlib).
- Path parameter `user_id` must match the authenticated user's ID from the JWT — raise 403 if mismatch.
- This step creates only a **skeleton endpoint** with placeholder assistant response — **no** real OpenAI Agents SDK, MCP server calls, tool execution, or AI generation yet.
- All database operations **MUST be async** using SQLModel `AsyncSession`.
- Use Pydantic v2 models for request/response validation.
- Conversation creation: Automatically create new `Conversation` row if no `conversation_id` provided.
- Message roles: "user" for incoming message, "assistant" for response.

## 2. Step 4 Overview & Goals

**Primary Objectives:**
- Implement a testable POST endpoint `/api/{user_id}/chat` that handles chat requests.
- Support new conversation creation and existing conversation resumption.
- Persist user messages immediately and assistant responses after generation.
- Return structured response matching exact Phase III requirements.
- Validate authentication and user ownership via JWT from Phase II.
- Provide foundation for later integration of OpenAI Agents SDK + MCP tools (Steps 5–6).

**Expected Outcomes:**
- Working endpoint that can be tested with curl/Postman.
- Conversations and messages correctly stored/retrieved from database.
- Stateless behavior verified (server restart → resume via conversation_id).
- Clear separation — AI/tool logic deferred to future steps.

## 3. Dependencies & Prerequisites

- Step 1: Database models (`Task`, `Conversation`, `Message`), async session utilities.
- Phase II JWT setup patterns (secret key, algorithm, token decoding logic — re-implemented in Phase III).
- Installed packages: `fastapi`, `uvicorn`, `pydantic`, `sqlmodel`, `python-jose[cryptography]`, `passlib[bcrypt]`.
- `.env` with: `DATABASE_URL`, `JWT_SECRET_KEY`, `JWT_ALGORITHM`.

## 4. Detailed Task Breakdown

### Task 4.1: Create Authentication Utilities Module
- **Description**: Set up the authentication utilities module with JWT handling and user validation
- **Inputs needed**: JWT secret key, algorithm from environment variables
- **Outputs/Files to generate**:
  - `phaseIII/backend/app/core/security.py` (JWT token handling, password hashing utilities)
  - `phaseIII/backend/app/api/deps.py` (authentication dependencies for FastAPI)
- **Dependencies**: None (initial task)
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create authentication utilities with JWT token handling, password hashing, and FastAPI dependencies for user authentication."

### Task 4.2: Create Chat Request/Response Models
- **Description**: Define Pydantic models for chat request and response validation
- **Inputs needed**: Specification for request/response structure
- **Outputs/Files to generate**:
  - `phaseIII/backend/app/schemas/chat.py` (ChatRequest and ChatResponse models)
- **Dependencies**: None (can be done independently)
- **Estimated complexity**: Low
- **Claude prompt hint**: "Create Pydantic models for ChatRequest and ChatResponse with proper validation fields."

### Task 4.3: Create Chat Service Layer
- **Description**: Implement the service layer that handles the business logic for chat operations
- **Inputs needed**: Database models, authentication utilities, request/response schemas
- **Outputs/Files to generate**:
  - `phaseIII/backend/app/services/chat.py` (service functions for chat operations)
- **Dependencies**: Tasks 4.1, 4.2, Step 1 database foundation
- **Estimated complexity**: High
- **Claude prompt hint**: "Create chat service layer with functions to handle conversation creation, message persistence, and placeholder assistant responses."

### Task 4.4: Create Chat API Endpoint
- **Description**: Implement the main chat API endpoint with authentication and business logic
- **Inputs needed**: Authentication utilities, request/response schemas, chat service
- **Outputs/Files to generate**:
  - `phaseIII/backend/app/api/v1/endpoints/chat.py` (the main chat endpoint)
- **Dependencies**: Tasks 4.1, 4.2, 4.3
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create the main chat endpoint at /api/{user_id}/chat with JWT authentication and integration with chat service."

### Task 4.5: Update Main Application File
- **Description**: Update the main application file to include the new chat router
- **Inputs needed**: Chat API endpoint
- **Outputs/Files to generate**:
  - `phaseIII/backend/app/main.py` (updated with chat routes)
- **Dependencies**: Task 4.4
- **Estimated complexity**: Low
- **Claude prompt hint**: "Update the main FastAPI application to include the chat API router."

### Task 4.6: Create Chat Endpoint Tests
- **Description**: Develop comprehensive tests for the chat endpoint functionality
- **Inputs needed**: Complete chat endpoint implementation
- **Outputs/Files to generate**:
  - `phaseIII/backend/tests/test_chat_endpoint.py` (tests for chat endpoint)
- **Dependencies**: Tasks 4.1-4.5
- **Estimated complexity**: Medium
- **Claude prompt hint**: "Create comprehensive tests for the chat endpoint covering authentication, conversation creation, and message persistence."

## 5. Risks & Mitigations

### Risk 1: Authentication Implementation Issues
- **Issue**: JWT token handling might have compatibility issues with Phase II patterns
- **Mitigation**: Carefully implement token decoding and validation based on proven patterns, with proper error handling.

### Risk 2: Database Transaction Problems
- **Issue**: Async database operations might have race conditions or transaction issues
- **Mitigation**: Use proper async session management with transaction handling, and implement retry mechanisms for transient failures.

### Risk 3: User ID Validation Failures
- **Issue**: Mismatch between path parameter user_id and authenticated user_id might not be caught properly
- **Mitigation**: Implement robust validation in the authentication dependency with clear error messages.

### Risk 4: Conversation State Management
- **Issue**: Conversation creation/resumption logic might have edge cases
- **Mitigation**: Thoroughly test the conversation lifecycle with multiple scenarios and implement proper error handling.

### Risk 5: Placeholder Response Limitations
- **Issue**: The placeholder assistant response might be too simplistic for testing
- **Mitigation**: Create a slightly more sophisticated placeholder that mimics real AI responses for better testing.

## 6. Success Criteria for Step 4
- Chat endpoint successfully handles POST requests at `/api/{user_id}/chat`
- Authentication properly validates JWT tokens and user_id matching
- Conversations are created when no conversation_id is provided
- Messages are properly stored in the database with correct roles
- Placeholder assistant response is returned with conversation_id and tool_calls
- Tests pass for all functionality
- Endpoint is stateless and works correctly after server restarts
- Integration-ready for Step 5 (OpenAI Agents SDK + MCP tools)

## 7. Next Actions
- Immediate next: Implement Task 4.1 (Authentication utilities) to establish the foundation
- Suggest prompt for first implementation task: "Based on this plan and previous spec, generate the code for Task 4.1: authentication utilities module with JWT handling and password hashing utilities in phaseIII/backend/app/core/security.py and phaseIII/backend/app/api/deps.py. Ensure async compatibility and proper error handling."
- After all tasks: Review full endpoint implementation, then move to Step 5 spec/plan (OpenAI Agents + MCP Integration)