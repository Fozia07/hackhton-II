---
id: 006
title: Create FastAPI Validation Security Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "validation", "security", "skill-creation", "pydantic", "error-handling"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-validation-security.md
tests:
  - none (documentation work)
---

## Prompt

write a skill for FastAPI Validation, Error Handling & Security Skill. Your responsibility is to ensure FastAPI APIs are safe, validated, and reliable. YOU HANDLE: - Pydantic request & response models - Input validation (body, query, path) - HTTPException usage - Global exception handlers - CORS and basic API security (if required)

## Response snapshot

Created comprehensive FastAPI Validation, Error Handling & Security skill documentation (21K) at `.claude/skills/fastapi-validation-security.md`.

The skill covers:

**1. Pydantic Request & Response Models**
- BaseModel definitions with field validation
- Custom validators using @field_validator decorator
- Response models with from_attributes configuration
- Nested models and complex validation patterns

**2. Input Validation**
- Request body validation with Pydantic models
- Query parameter validation with type hints and constraints
- Path parameter validation with regex patterns
- File upload validation
- Custom validation logic

**3. HTTPException Usage**
- Standard HTTP status codes (400, 401, 403, 404, 422, 500)
- Custom error responses with detail messages
- Exception raising patterns in endpoints

**4. Global Exception Handlers**
- RequestValidationError handler for 422 errors
- Database exception handlers (IntegrityError, OperationalError)
- General exception handler for 500 errors
- Custom exception classes (BusinessLogicError, ResourceNotFoundError)

**5. CORS Configuration**
- Basic CORS setup for development
- Production CORS with specific origins
- Dynamic CORS with environment-based configuration
- Credential and header handling

**6. Security Implementations**
- JWT authentication (token creation, validation, dependencies)
- Role-based authorization with UserRole enum
- Permission-based authorization with decorators
- Security best practices:
  - Input sanitization
  - Rate limiting with slowapi
  - Security headers (HSTS, CSP, X-Frame-Options)
  - API key authentication

**7. Testing Patterns**
- Validation testing with TestClient
- Authentication testing with JWT tokens
- Error handling testing
- Security testing for unauthorized access

The skill integrates seamlessly with fastapi-core-routing.md and sqlmodel.md skills, providing the validation and security layer for FastAPI applications.

## Outcome

- ✅ Impact: Created production-ready FastAPI validation and security skill with comprehensive examples and best practices
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-validation-security.md (21K)
- 🔁 Next prompts: User may request additional FastAPI skills (middleware, background tasks, WebSockets) or begin implementing a FastAPI application using these skills
- 🧠 Reflection: This skill complements the existing FastAPI Core & Routing skill, providing a complete foundation for building secure, validated FastAPI applications. The comprehensive coverage of Pydantic validation, exception handling, and security patterns ensures developers can build production-ready APIs.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
