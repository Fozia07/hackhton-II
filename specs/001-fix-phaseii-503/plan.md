# Implementation Plan: Fix Phase II Authentication 503 Error

**Branch**: `001-fix-phaseii-503` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fix-phaseii-503/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix the 503 error occurring during Phase II signin/signup operations. The primary issue is that the frontend is configured to call a remote Hugging Face Space URL (`https://fozi07-todo-full-stack-app.hf.space`) instead of the local backend running on port 8001. This causes all authentication requests to fail with 503 errors when the remote service is unavailable, while the local backend receives no requests and logs nothing. Secondary issues include CORS configuration not including localhost:3001 and missing deployment readiness documentation.

**Technical Approach**:
1. Update frontend environment configuration to point to local backend (http://localhost:8001)
2. Update backend CORS configuration to include localhost:3001
3. Verify backend startup and logging configuration
4. Document all dependencies for deployment readiness
5. Implement comprehensive health check endpoint
6. Test end-to-end authentication flows

## Technical Context

**Language/Version**:
- Backend: Python 3.11+ with FastAPI 0.115+
- Frontend: TypeScript 5.9+ with Next.js 16.1.1 (Turbopack)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, asyncpg, python-jose[cryptography], passlib[bcrypt], uvicorn
- Frontend: Next.js, React 19, TanStack Query, Tailwind CSS 4.1, Zod

**Storage**: PostgreSQL (Neon hosted) via asyncpg driver

**Testing**:
- Backend: pytest with pytest-asyncio
- Frontend: Next.js built-in testing (not yet implemented)
- Manual E2E testing for authentication flows

**Target Platform**:
- Backend: Cloud deployment (Railway/Render/Vercel) with Python 3.11+ runtime
- Frontend: Vercel deployment with Node.js 20+ runtime

**Project Type**: Web application (separate backend and frontend)

**Performance Goals**:
- Authentication requests complete within 2 seconds under normal load
- Backend startup within 10 seconds
- Health check response within 500ms

**Constraints**:
- Must maintain backward compatibility with existing Phase II user accounts
- Must not modify Phase III authentication system
- Must use existing authentication libraries (no major refactoring)
- Must preserve existing user data during fixes

**Scale/Scope**:
- Development environment (localhost)
- Small user base (< 100 concurrent users expected)
- 2 authentication endpoints (signup, signin)
- 1 health check endpoint

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Review

✅ **Spec-Driven Development**: Feature has complete specification with user stories, functional requirements, and success criteria

✅ **Smallest Viable Change**: Fix focuses only on 503 error and deployment readiness, no unnecessary refactoring

✅ **Testable Requirements**: All functional requirements (FR-001 to FR-015) are testable with clear acceptance criteria

✅ **Clear Acceptance Criteria**: Each user story has detailed acceptance scenarios

✅ **No Implementation Leakage**: Specification focuses on user value and business needs, not technical implementation

✅ **Explicit Error Paths**: Edge cases documented (9 scenarios) including backend unavailability, concurrent requests, database failures

✅ **Code References**: Will be added during implementation phase with file:line format

⚠️ **Dependency Management**: Need to verify all dependencies are documented and separated (dev vs production)

### Constitution Principles Applied

1. **Clarify and Plan First**: Complete specification created before planning
2. **Human as Tool**: Will invoke user for clarification if additional issues discovered during research
3. **Authoritative Source Mandate**: Will use MCP tools and CLI commands for verification
4. **Knowledge Capture**: PHR will be created after plan completion
5. **Explicit ADR Suggestions**: Will suggest ADR if significant architectural decisions emerge

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-phaseii-503/
├── spec.md                    # Feature specification (completed)
├── plan.md                    # This file (in progress)
├── research.md                # Phase 0 output (to be created)
├── data-model.md              # Phase 1 output (to be created)
├── quickstart.md              # Phase 1 output (to be created)
├── contracts/                 # Phase 1 output (to be created)
│   ├── auth-signup.md         # POST /auth/signup contract
│   ├── auth-signin.md         # POST /auth/signin contract
│   └── health-check.md        # GET /health contract
├── checklists/
│   └── requirements.md        # Validation checklist (completed)
└── tasks.md                   # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
phaseII/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py           # Settings and environment configuration
│   │   │   ├── database.py         # Database session management
│   │   │   └── security.py         # JWT and password hashing utilities
│   │   ├── models/
│   │   │   ├── user.py             # User model and schemas
│   │   │   └── todo.py             # Todo model and schemas
│   │   ├── routes/
│   │   │   ├── auth.py             # Authentication endpoints (signup, signin)
│   │   │   └── todos.py            # Todo CRUD endpoints
│   │   └── main.py                 # FastAPI application and CORS configuration
│   ├── tests/
│   │   ├── test_auth.py            # Authentication endpoint tests (to be created)
│   │   └── test_todos.py           # Todo endpoint tests (existing)
│   ├── .env                        # Environment variables (local development)
│   ├── .env.example                # Environment template
│   ├── .env.production             # Production environment template
│   ├── requirements.txt            # Python dependencies (to be verified)
│   └── README.md                   # Backend documentation (to be created)
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── login/              # Login page
    │   │   ├── signup/             # Signup page
    │   │   └── dashboard/          # Dashboard page
    │   ├── components/             # Reusable UI components
    │   ├── lib/
    │   │   └── api.ts              # API client configuration
    │   └── types/                  # TypeScript type definitions
    ├── .env.local                  # Local environment (NEEDS FIX)
    ├── .env.example                # Environment template
    ├── .env.production             # Production environment
    ├── package.json                # Node.js dependencies
    └── README.md                   # Frontend documentation (to be created)
```

**Structure Decision**: Web application structure with separate backend (FastAPI) and frontend (Next.js). Backend follows FastAPI best practices with core utilities, models, and routes separation. Frontend follows Next.js 13+ App Router structure with app directory for pages and components for reusable UI.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are being followed.

---

# Phase 0: Research

**Goal**: Investigate root causes of 503 error, verify backend configuration, and document current state.

**Deliverable**: `research.md` with findings and recommendations.

## Research Tasks

### R0.1: Investigate Frontend Configuration
**Objective**: Identify why frontend shows 503 error while backend logs nothing

**Actions**:
1. Read `phaseII/frontend/.env.local` and verify API URL configuration
2. Read `phaseII/frontend/.env.example` and `.env.production` for comparison
3. Search for API client configuration in `phaseII/frontend/src/lib/api.ts` or similar
4. Verify which environment variable is used for backend URL (NEXT_PUBLIC_API_URL)
5. Document current configuration vs expected configuration

**Expected Findings**:
- Frontend is configured to call remote Hugging Face Space URL instead of localhost:8001
- This explains why backend receives no requests and logs nothing
- Fix requires updating .env.local to point to http://localhost:8001

**Tools**: Read, Grep

---

### R0.2: Verify Backend Startup and Logging
**Objective**: Ensure backend starts correctly and logs all requests

**Actions**:
1. Read `phaseII/backend/app/main.py` to verify logging configuration
2. Check if uvicorn is configured with proper logging level
3. Verify FastAPI middleware logs incoming requests
4. Test backend startup by running: `cd phaseII/backend && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`
5. Test health check endpoint: `curl http://localhost:8001/health`
6. Document current logging behavior

**Expected Findings**:
- Backend has basic logging configured (logging.basicConfig)
- May need to add request logging middleware for debugging
- Health check endpoint exists but may need enhancement

**Tools**: Read, Bash

---

### R0.3: Analyze CORS Configuration
**Objective**: Verify CORS allows requests from frontend on localhost:3001

**Actions**:
1. Read `phaseII/backend/app/main.py` CORS middleware configuration
2. Read `phaseII/backend/app/core/config.py` for allowed_origins setting
3. Verify if localhost:3001 is included in allowed origins
4. Check if CORS is configured for preflight OPTIONS requests
5. Document current CORS configuration vs required configuration

**Expected Findings**:
- CORS configuration exists but may not include localhost:3001
- Hardcoded origins in main.py override settings from config.py
- Need to add localhost:3001 to allowed origins list

**Tools**: Read, Grep

---

### R0.4: Review Authentication Implementation
**Objective**: Understand current authentication flow and identify potential issues

**Actions**:
1. Read `phaseII/backend/app/routes/auth.py` for signup and signin endpoints
2. Read `phaseII/backend/app/core/security.py` for JWT and password hashing
3. Read `phaseII/backend/app/models/user.py` for User model
4. Verify error handling and logging in authentication endpoints
5. Check if endpoints return proper HTTP status codes
6. Document authentication flow and any issues found

**Expected Findings**:
- Authentication endpoints exist and appear well-implemented
- Proper error handling with HTTPException
- Logging exists for debugging
- No obvious issues in authentication logic

**Tools**: Read

---

### R0.5: Verify Database Configuration
**Objective**: Ensure database connection is properly configured

**Actions**:
1. Read `phaseII/backend/.env` for DATABASE_URL
2. Read `phaseII/backend/app/core/database.py` for connection configuration
3. Verify asyncpg driver is used for PostgreSQL
4. Check if database tables are created on startup (lifespan function)
5. Test database connection by calling /test-db endpoint
6. Document database configuration

**Expected Findings**:
- Database URL is configured for Neon PostgreSQL
- asyncpg driver is used correctly
- Tables are created on startup via lifespan function
- Database connection should be working

**Tools**: Read, Bash

---

### R0.6: Document Dependencies
**Objective**: List all dependencies for deployment readiness

**Actions**:
1. Read `phaseII/backend/requirements.txt` (or check if it exists)
2. If requirements.txt doesn't exist, generate it from installed packages
3. Separate development dependencies from production dependencies
4. Read `phaseII/frontend/package.json` for Node.js dependencies
5. Verify all dependencies are compatible with deployment platforms
6. Document dependency management strategy

**Expected Findings**:
- May need to create or update requirements.txt
- Need to separate dev dependencies (pytest, etc.) from production
- Frontend dependencies are properly managed in package.json

**Tools**: Read, Bash

---

### R0.7: Test Current Authentication Flow
**Objective**: Reproduce the 503 error and document exact behavior

**Actions**:
1. Start backend: `cd phaseII/backend && uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload`
2. Start frontend: `cd phaseII/frontend && npm run dev`
3. Open browser to http://localhost:3001/signup
4. Attempt to create a new account
5. Monitor backend logs for any incoming requests
6. Monitor browser network tab for request details
7. Document exact error message and behavior

**Expected Findings**:
- Frontend makes request to remote Hugging Face Space URL
- Request fails with 503 (service unavailable)
- Backend receives no requests and logs nothing
- Confirms root cause is frontend misconfiguration

**Tools**: Bash, manual testing

---

## Research Deliverable Structure

```markdown
# Research: Fix Phase II Authentication 503 Error

## Executive Summary
[Brief overview of findings and root cause]

## Investigation Results

### Frontend Configuration Issue (R0.1)
- **Current State**: [findings]
- **Root Cause**: [explanation]
- **Recommendation**: [fix]

### Backend Startup and Logging (R0.2)
- **Current State**: [findings]
- **Issues Found**: [list]
- **Recommendation**: [improvements]

### CORS Configuration (R0.3)
- **Current State**: [findings]
- **Issues Found**: [list]
- **Recommendation**: [fix]

### Authentication Implementation (R0.4)
- **Current State**: [findings]
- **Issues Found**: [list]
- **Recommendation**: [improvements if any]

### Database Configuration (R0.5)
- **Current State**: [findings]
- **Issues Found**: [list]
- **Recommendation**: [improvements if any]

### Dependencies Documentation (R0.6)
- **Current State**: [findings]
- **Missing Dependencies**: [list]
- **Recommendation**: [documentation needed]

### Authentication Flow Testing (R0.7)
- **Test Results**: [findings]
- **Error Reproduction**: [exact steps and error]
- **Confirmation**: [root cause confirmed]

## Recommendations for Phase 1

1. **Critical Fixes**:
   - Update frontend .env.local to point to http://localhost:8001
   - Add localhost:3001 to backend CORS allowed origins

2. **Enhancements**:
   - Add request logging middleware to backend
   - Enhance health check endpoint with detailed status
   - Document all dependencies in requirements.txt

3. **Documentation**:
   - Create deployment guide
   - Document environment variable requirements
   - Create troubleshooting guide

## Open Questions
[Any questions that need user clarification]
```

---

# Phase 1: Design

**Goal**: Create detailed design artifacts for implementing the fix.

**Deliverables**:
- `data-model.md` - Data structures and schemas
- `contracts/` - API endpoint contracts
- `quickstart.md` - Setup and deployment guide

## Design Tasks

### D1.1: Data Model Documentation
**Objective**: Document existing data models and any changes needed

**Deliverable**: `data-model.md`

**Content**:
1. User model schema (existing)
2. Authentication request/response schemas (existing)
3. Health check response schema (to be enhanced)
4. Error response schemas (existing)
5. No changes to data models required for this fix

**Tools**: Read existing models, document in markdown

---

### D1.2: API Contract Specifications
**Objective**: Document API contracts for all authentication endpoints

**Deliverable**: `contracts/` directory with individual contract files

**Contracts to Create**:

1. **auth-signup.md**:
   - Endpoint: POST /auth/signup
   - Request body schema (UserCreate)
   - Response schema (UserRead)
   - Error responses (400, 409, 500)
   - Example requests and responses

2. **auth-signin.md**:
   - Endpoint: POST /auth/signin
   - Request body schema (UserSignIn)
   - Response schema (access_token, token_type, user_id, username)
   - Error responses (401, 500)
   - Example requests and responses

3. **health-check.md**:
   - Endpoint: GET /health
   - Response schema (status, database, timestamp)
   - Success response (200)
   - Error response (500)
   - Example responses

**Tools**: Read existing code, create contract documentation

---

### D1.3: Environment Configuration Design
**Objective**: Design proper environment configuration for all environments

**Deliverable**: Part of `quickstart.md`

**Configuration Files**:

1. **Backend .env**:
   ```
   APP_TITLE=Phase 2 Backend
   APP_VERSION=0.1.0
   DEBUG=False
   DATABASE_URL=postgresql+asyncpg://...
   JWT_SECRET_KEY=<secure-key>
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002,https://hackhton-ii.vercel.app
   ```

2. **Frontend .env.local**:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8001
   NEXT_PUBLIC_APP_URL=http://localhost:3001
   NODE_ENV=development
   ```

3. **Frontend .env.production**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
   NEXT_PUBLIC_APP_URL=https://hackhton-ii.vercel.app
   NODE_ENV=production
   ```

**Tools**: Document configuration requirements

---

### D1.4: Deployment Readiness Design
**Objective**: Design deployment strategy and document requirements

**Deliverable**: Part of `quickstart.md`

**Deployment Requirements**:

1. **Backend Deployment** (Railway/Render):
   - Python 3.11+ runtime
   - Install production dependencies only
   - Set environment variables
   - Run database migrations
   - Health check endpoint for monitoring

2. **Frontend Deployment** (Vercel):
   - Node.js 20+ runtime
   - Set NEXT_PUBLIC_API_URL to backend URL
   - Build and deploy

3. **Dependencies**:
   - Create requirements.txt with production dependencies
   - Create requirements-dev.txt with development dependencies
   - Document all environment variables

**Tools**: Document deployment process

---

### D1.5: Enhanced Health Check Design
**Objective**: Design comprehensive health check endpoint

**Deliverable**: Part of `contracts/health-check.md`

**Health Check Response**:
```json
{
  "status": "ok",
  "timestamp": "2026-02-07T12:00:00Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 15
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

**Implementation Notes**:
- Test database connectivity with actual query
- Measure database latency
- Return 200 for healthy, 503 for unhealthy
- Include version information

**Tools**: Design document

---

### D1.6: Request Logging Middleware Design
**Objective**: Design request logging for debugging

**Deliverable**: Part of `quickstart.md`

**Logging Requirements**:
1. Log all incoming requests with method, path, client IP
2. Log request processing time
3. Log response status code
4. Log authentication attempts (success/failure)
5. Never log passwords or sensitive data

**Implementation Approach**:
- Add FastAPI middleware for request logging
- Use Python logging module with INFO level
- Format: `[timestamp] method path status_code duration_ms`

**Tools**: Design document

---

## Design Deliverable Structure

### data-model.md
```markdown
# Data Models: Fix Phase II Authentication 503 Error

## User Model
[Schema documentation]

## Authentication Schemas
[Request/response schemas]

## Health Check Schema
[Enhanced health check response]

## Error Schemas
[Standard error responses]
```

### contracts/auth-signup.md
```markdown
# API Contract: POST /auth/signup

## Endpoint
POST /auth/signup

## Request
[Schema and example]

## Response
[Schema and examples for success and errors]

## Error Codes
[List of possible errors]
```

### quickstart.md
```markdown
# Quickstart Guide: Phase II Authentication

## Prerequisites
[Requirements]

## Local Development Setup
[Step-by-step setup]

## Environment Configuration
[Configuration details]

## Running the Application
[Commands to start backend and frontend]

## Testing Authentication
[How to test signup and signin]

## Deployment
[Deployment instructions]

## Troubleshooting
[Common issues and solutions]
```

---

# Phase 2: Task Generation

**Note**: Phase 2 (task generation) is handled by the `/sp.tasks` command, NOT by `/sp.plan`.

After Phase 1 design artifacts are complete, run `/sp.tasks` to generate the implementation tasks in `tasks.md`.

The tasks will be generated based on:
- Functional requirements from spec.md
- Design artifacts from Phase 1 (data-model.md, contracts/, quickstart.md)
- Research findings from Phase 0 (research.md)

Expected task categories:
1. **Configuration Tasks**: Fix frontend .env.local, update backend CORS
2. **Enhancement Tasks**: Add request logging, enhance health check
3. **Documentation Tasks**: Create requirements.txt, update README files
4. **Testing Tasks**: Test authentication flows end-to-end
5. **Deployment Tasks**: Document deployment process

---

# Architectural Decisions

## AD-001: Frontend Environment Configuration Strategy

**Context**: Frontend was configured to call remote Hugging Face Space URL instead of local backend, causing 503 errors.

**Decision**: Use environment variables (NEXT_PUBLIC_API_URL) to configure backend URL, with separate .env files for local development (.env.local) and production (.env.production).

**Rationale**:
- Allows easy switching between local and deployed backends
- Follows Next.js best practices for environment configuration
- Prevents hardcoding URLs in source code
- Enables different configurations per environment

**Alternatives Considered**:
1. Hardcode URLs in source code - Rejected: Not flexible, requires code changes for different environments
2. Use single .env file - Rejected: Doesn't support multiple environments
3. Use runtime configuration - Rejected: More complex, not needed for this use case

**Consequences**:
- Developers must ensure .env.local is configured correctly
- Documentation must clearly explain environment variable requirements
- Deployment process must set correct environment variables

**Status**: Accepted

---

## AD-002: CORS Configuration Approach

**Context**: Backend CORS configuration had hardcoded origins that didn't include localhost:3001.

**Decision**: Use environment variable (ALLOWED_ORIGINS) for CORS configuration, but ensure main.py properly parses and uses this variable instead of hardcoding origins.

**Rationale**:
- Allows flexible CORS configuration without code changes
- Supports multiple frontend origins (local development, staging, production)
- Follows security best practice of explicitly allowing origins
- Easier to maintain and update

**Alternatives Considered**:
1. Allow all origins (*) - Rejected: Security risk, not suitable for production
2. Hardcode all possible origins - Rejected: Not maintainable, requires code changes
3. Use wildcard patterns - Rejected: Not supported by CORS spec for credentials

**Consequences**:
- Must ensure ALLOWED_ORIGINS includes all required origins
- Must update CORS middleware to properly use environment variable
- Documentation must explain CORS configuration

**Status**: Accepted

---

## AD-003: Dependency Management Strategy

**Context**: Need to ensure backend is deployment-ready with proper dependency management.

**Decision**: Use requirements.txt for production dependencies and requirements-dev.txt for development dependencies. Use pip-tools (pip-compile) for dependency pinning.

**Rationale**:
- Separates production and development dependencies
- Ensures reproducible builds with pinned versions
- Follows Python best practices
- Compatible with all deployment platforms

**Alternatives Considered**:
1. Single requirements.txt - Rejected: Includes unnecessary dev dependencies in production
2. Poetry - Rejected: Adds complexity, not needed for this project
3. Pipenv - Rejected: Less widely supported on deployment platforms

**Consequences**:
- Must maintain two requirements files
- Must document which file to use for which purpose
- Deployment process must use requirements.txt only

**Status**: Accepted

---

# Risk Assessment

## Technical Risks

### Risk 1: Frontend Still Shows 503 After Configuration Fix
**Likelihood**: Low
**Impact**: High
**Mitigation**:
- Verify browser cache is cleared after .env.local change
- Restart Next.js dev server after configuration change
- Test with curl to verify backend is accessible
- Check browser network tab for actual URL being called

---

### Risk 2: CORS Preflight Requests Fail
**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Ensure OPTIONS method is included in allowed methods
- Verify CORS middleware is configured before route handlers
- Test with browser developer tools network tab
- Add logging for CORS-related requests

---

### Risk 3: Database Connection Fails in Production
**Likelihood**: Low
**Impact**: High
**Mitigation**:
- Test database connection with health check endpoint
- Verify DATABASE_URL is correctly set in production environment
- Ensure SSL mode is enabled for Neon PostgreSQL
- Add database connection retry logic

---

### Risk 4: Missing Dependencies in Production
**Likelihood**: Medium
**Impact**: High
**Mitigation**:
- Create comprehensive requirements.txt with all dependencies
- Test deployment in clean environment before production
- Document all required environment variables
- Use health check endpoint to verify all services are operational

---

## User Impact Risks

### Risk 5: Existing User Sessions Invalidated
**Likelihood**: Low
**Impact**: Low
**Mitigation**:
- No changes to JWT secret key or authentication logic
- Existing tokens remain valid
- Users may need to re-login if frontend URL changes

---

### Risk 6: Downtime During Configuration Changes
**Likelihood**: Low
**Impact**: Low
**Mitigation**:
- Configuration changes can be made without downtime
- Test all changes in development environment first
- Have rollback plan ready

---

# Success Criteria Mapping

This section maps functional requirements from spec.md to implementation phases:

## Phase 0 Research
- **FR-003**: Verify backend logging configuration
- **FR-004**: Verify authentication processing logging
- **FR-009**: Verify backend accessibility
- **FR-010**: Verify CORS configuration

## Phase 1 Design
- **FR-011**: Document all dependencies
- **FR-012**: Design health check endpoint
- **FR-013**: Design health check implementation
- **FR-014**: Design deployment process
- **FR-015**: Design dependency separation

## Phase 2 Implementation (via /sp.tasks)
- **FR-001**: Fix frontend configuration to enable signup
- **FR-002**: Fix frontend configuration to enable signin
- **FR-005**: Fix frontend-backend connection
- **FR-006**: Verify input validation (existing)
- **FR-007**: Verify HTTP status codes (existing)
- **FR-008**: Verify error messages (existing)

---

# Next Steps

1. **Complete Phase 0 Research**: Execute all research tasks (R0.1 - R0.7) and create research.md
2. **Complete Phase 1 Design**: Create all design artifacts (data-model.md, contracts/, quickstart.md)
3. **Run /sp.tasks**: Generate implementation tasks based on research and design
4. **Execute Tasks**: Implement fixes and enhancements
5. **Test End-to-End**: Verify authentication flows work correctly
6. **Create PHR**: Document this planning session
7. **Consider ADR**: Evaluate if architectural decisions warrant formal ADR documentation

---

# Appendix

## Key Files to Modify

1. **phaseII/frontend/.env.local** - Update NEXT_PUBLIC_API_URL to http://localhost:8001
2. **phaseII/backend/app/main.py** - Update CORS configuration to use environment variable
3. **phaseII/backend/requirements.txt** - Create/update with production dependencies
4. **phaseII/backend/requirements-dev.txt** - Create with development dependencies
5. **phaseII/backend/app/main.py** - Add request logging middleware
6. **phaseII/backend/app/main.py** - Enhance health check endpoint

## Key Files to Create

1. **specs/001-fix-phaseii-503/research.md** - Research findings
2. **specs/001-fix-phaseii-503/data-model.md** - Data model documentation
3. **specs/001-fix-phaseii-503/quickstart.md** - Setup and deployment guide
4. **specs/001-fix-phaseii-503/contracts/auth-signup.md** - Signup endpoint contract
5. **specs/001-fix-phaseii-503/contracts/auth-signin.md** - Signin endpoint contract
6. **specs/001-fix-phaseii-503/contracts/health-check.md** - Health check contract
7. **phaseII/backend/README.md** - Backend documentation
8. **phaseII/frontend/README.md** - Frontend documentation

## References

- Spec: [specs/001-fix-phaseii-503/spec.md](./spec.md)
- Requirements Checklist: [specs/001-fix-phaseii-503/checklists/requirements.md](./checklists/requirements.md)
- Constitution: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
