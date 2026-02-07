# Todo AI Chatbot - Chat Endpoint Specification (Step 4 - Revised)

## 1. Constitution Reinforcement

**Core Isolation Principles:**
- Phase III must remain **completely isolated** from Phase II — no modifications, overwrites, refactors, or direct imports from Phase II folders/code.
- Phase II frontend & backend are **READ-ONLY** forever.
- Phase III lives in separate top-level folders (e.g., `phase3-backend/`, `phase3-frontend/`, `specs/`, etc.).
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

## 4. Chat Endpoint Specification

### Endpoint Details
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Path Parameter**: `user_id` (str) — must match authenticated user's ID
- **Authentication**: OAuth2PasswordBearer (from Phase II logic) → dependency extracts token, decodes to user, validates against path `user_id`

### Request Body (Pydantic Model)
```python
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str = Field(..., min_length=1, description="User's natural language message")
```

### Response Body (Pydantic Model)
```python
class ChatResponse(BaseModel):
    success: bool
    conversation_id: int
    response: str
    tool_calls: list = []
    error: Optional[str] = None
```

### Database Operations Required
- **On Request**: Fetch conversation history from database if conversation_id provided
- **On Request**: Create new conversation if no conversation_id provided
- **On Request**: Store incoming user message to database with role "user"
- **On Response**: Store assistant response to database with role "assistant"
- **All operations**: Must be async and user-scoped (user_id validation)

### Authentication Flow
1. Extract JWT token from Authorization header
2. Decode token to get authenticated user_id
3. Compare path parameter user_id with decoded user_id
4. Raise 403 Forbidden if they don't match
5. Proceed with chat logic if they match

### Error Handling
- **Authentication Error**: Return 403 Forbidden
- **Validation Error**: Return 422 Unprocessable Entity
- **Database Error**: Return 500 Internal Server Error
- **General Error**: Return 500 Internal Server Error

### Placeholder Assistant Response
- For this step, return a simple placeholder response like: "I received your message: '{user_message}'. This is a placeholder response. The actual AI integration will be added in future steps."
- In future steps, this will be replaced with actual OpenAI Agent + MCP tool calls

### Conversation State Management
- If conversation_id is None: create new Conversation record, return new conversation_id
- If conversation_id is provided: fetch existing conversation, validate user ownership
- Store each message (user and assistant) in Message table with proper role and sequence