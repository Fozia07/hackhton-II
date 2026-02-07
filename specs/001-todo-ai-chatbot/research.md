# Todo AI Chatbot - Research Document

## Phase II Database Analysis

### Task Model Investigation
**Decision**: Verify if Phase II Task model already includes user_id for scoping
**Rationale**: Need to determine if additional migration is required or if existing model can be reused
**Findings**:
- Phase II likely has a Task model with user association for multi-tenancy
- Need to confirm if user_id field exists and is properly indexed
- If user_id exists, MCP tools can leverage existing scoping
- If not, need to create migration to add user_id field with proper indexing

### Neon DB Connection Details
**Decision**: Determine exact database URL and connection parameters
**Rationale**: Phase III needs to connect to the same Neon database as Phase II
**Findings**:
- Need to check Phase II backend/railway.json or similar config files
- Verify database credentials and connection pooling settings
- Ensure Phase III uses separate connection pool to avoid conflicts

### Authentication System Compatibility
**Decision**: Understand how Phase II handles user authentication for scoping
**Rationale**: MCP tools need to properly authenticate and identify users
**Findings**:
- Phase II likely uses JWT tokens with user identity claims
- Need to understand token structure to extract user_id
- Verify if authentication middleware is available for reuse

## Technology Stack Recommendations

### Database ORM Selection
**Decision**: Use SQLModel as recommended in the original requirements
**Rationale**: SQLModel provides Pydantic-like validation with SQLAlchemy power
**Alternatives considered**:
- Pure SQLAlchemy: More complex, no Pydantic integration
- Tortoise ORM: Async-first but less mature
- Peewee: Simpler but lacks modern typing features

### Migration Tool
**Decision**: Use Alembic for database migrations
**Rationale**: Industry standard for SQLAlchemy-based applications
**Alternatives considered**:
- Flask-Migrate: Tied to Flask ecosystem
- Manual SQL: Error-prone and not version-controlled
- Django migrations: Not applicable to FastAPI

### Async Framework
**Decision**: Use FastAPI for the backend
**Rationale**: High-performance, automatic API documentation, Pydantic integration
**Alternatives considered**:
- Flask: Synchronous by default, slower
- Django: Heavy framework for microservice needs
- Starlette: Too low-level without FastAPI's conveniences

## MCP Server Architecture

### Model Design Approach
**Decision**: Create separate tables for chat persistence while reusing Task model
**Rationale**: Maintains separation of concerns while leveraging existing infrastructure
**Details**:
- Conversation table: Tracks individual chat sessions
- Message table: Stores chat messages with user/agent distinction
- AgentInteraction table: Logs MCP tool invocations and results
- Task table: Reused from Phase II with proper scoping

### Safety Measures
**Decision**: Implement strict user_id scoping across all operations
**Rationale**: Prevents cross-user data leakage and ensures privacy
**Implementation**:
- All queries must include user_id filter
- Foreign key relationships enforce user ownership
- Business logic layer validates user access