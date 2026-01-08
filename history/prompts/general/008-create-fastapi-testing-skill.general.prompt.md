---
id: 008
title: Create FastAPI Testing Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "testing", "skill-creation", "pytest", "testclient", "mocking"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-testing.md
tests:
  - none (documentation work)
---

## Prompt

Continue (implicit: continue building FastAPI skills ecosystem)

## Response snapshot

Created comprehensive FastAPI Testing skill documentation (26K) at `.claude/skills/fastapi-testing.md`.

The skill covers:

**1. TestClient Setup**
- Basic TestClient usage for endpoint testing
- TestClient with context manager for proper cleanup
- Request/response testing patterns

**2. Pytest Fixtures**
- Basic fixtures for session, settings, and client
- Advanced fixtures with async support
- Fixture scopes (function, module, session)
- Dependency override patterns

**3. Testing CRUD Operations**
- Create operations with validation
- Read operations with 404 handling
- Update operations with partial updates
- Delete operations with verification
- List operations with pagination
- Duplicate detection and error cases

**4. Testing Authentication and Authorization**
- Authentication fixtures (test_user, admin_user, auth_token, admin_token)
- Login testing (success, invalid credentials, user not found)
- Protected endpoint testing (without token, with valid/invalid/expired token)
- Role-based authorization testing (user vs admin access)

**5. Testing Validation and Error Handling**
- Request validation (invalid email, weak password, missing fields)
- Query parameter validation (invalid pagination, limits)
- Custom business logic error testing

**6. Mocking External Dependencies**
- Mocking external API calls with unittest.mock
- Mocking email service for registration flows
- Mocking Redis cache operations
- Verification of mock calls

**7. Integration Testing**
- Complete user workflow testing (register → login → profile → update → delete)
- Testing relationships and foreign keys
- Multi-endpoint integration scenarios

**8. Testing Async Endpoints**
- Async endpoint testing with pytest.mark.asyncio
- Async database operation testing

**9. Testing Background Tasks**
- Background task trigger verification
- Mock-based background task testing

**Best Practices**:
- Test organization (descriptive names, one assertion per test)
- Test isolation (independent tests, fixtures, no execution order dependency)
- Test coverage (80%+ target, error paths, edge cases)
- Test data (factories, realistic data, cleanup)
- Mocking strategy (mock external dependencies, verify calls)

**Running Tests**:
- pytest commands (basic, coverage, specific tests, patterns, parallel)
- pytest.ini configuration with coverage thresholds and markers

The skill completes the testing layer for FastAPI applications, integrating with all previously created skills (core-routing, validation-security, config-logging, sqlmodel).

## Outcome

- ✅ Impact: Created production-ready FastAPI testing skill with comprehensive patterns for unit tests, integration tests, authentication testing, mocking, and coverage measurement
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-testing.md (26K)
- 🔁 Next prompts: User may request additional FastAPI skills (database migrations, background tasks, WebSockets, middleware, file handling) or begin implementing a FastAPI application with full test coverage
- 🧠 Reflection: This skill completes the core development cycle for FastAPI applications. Combined with the existing skills (routing, validation/security, configuration/logging, database, testing), developers now have a complete toolkit for building, securing, configuring, and testing production-ready FastAPI applications with comprehensive test coverage.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
