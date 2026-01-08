---
id: 013
title: Create JWT Better Auth Integration Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["jwt", "better-auth", "authentication", "skill-creation", "nextjs", "fastapi", "integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/jwt-better-auth-integration.md
tests:
  - none (documentation work)
---

## Prompt

creating a reusable SKILL for an agentic development system.

SKILL NAME:
JWT & Better Auth Integration Skill

CONTEXT:
This skill will be used in a spec-driven, monorepo-based full-stack project.
Frontend uses Next.js (App Router) with Better Auth.
Backend uses FastAPI.
Authentication must be stateless using JWT.

GOAL:
Create a reusable authentication skill that securely integrates
Better Auth (frontend) with FastAPI (backend) using JWT tokens.

RESPONSIBILITIES OF THIS SKILL:
- Configure Better Auth to issue JWT tokens
- Define how JWT tokens are attached to frontend API requests
- Define how FastAPI verifies JWT tokens
- Extract authenticated user identity from JWT
- Enforce user-level authorization on all API routes
- Handle authentication errors correctly

FRONTEND SCOPE (Next.js + Better Auth):
- Enable Better Auth JWT plugin
- Issue JWT on login/signup
- Attach JWT to every backend request using: Authorization: Bearer <token>
- Handle token expiry gracefully
- Never expose secrets in client code

BACKEND SCOPE (FastAPI):
- Read JWT from Authorization header
- Verify JWT signature using shared secret
- Validate token expiry and claims
- Decode user_id / email from token
- Reject requests with missing or invalid tokens (401)
- Reject cross-user access attempts (403)
- Provide a reusable auth dependency/middleware

JWT RULES:
- Algorithm: HS256
- Secret key from environment variable: BETTER_AUTH_SECRET
- Token must include: user_id (or sub), email, exp

## Response snapshot

Created comprehensive JWT & Better Auth Integration skill documentation (30K) at `.claude/skills/jwt-better-auth-integration.md`.

The skill covers:

**Authentication Flow**:
- Complete flow from login → JWT issuance → token attachment → verification → user extraction
- JWT token structure with sub, email, exp, iat claims

**Frontend Implementation (Next.js + Better Auth)**:
1. Better Auth configuration with JWT plugin
   - JWT secret from environment
   - Token expiration (1 hour)
   - HS256 algorithm
   - Custom payload with user_id and email

2. Better Auth API route setup
   - Auth handler at /api/auth/[...all]

3. Client-side auth hook
   - createAuthClient with signIn, signUp, signOut, useSession

4. API client with automatic JWT attachment
   - getJWTToken() to fetch JWT from Better Auth
   - apiFetch() wrapper that attaches Authorization: Bearer <token>
   - Automatic 401/403 error handling
   - Convenience methods (get, post, put, delete)

5. JWT token generation endpoint
   - /api/auth/get-jwt endpoint
   - Validates session and generates JWT

6. Component usage examples
   - UserProfile component with useSession and api.get()

**Backend Implementation (FastAPI)**:
1. JWT configuration
   - Settings with BETTER_AUTH_SECRET (must match frontend)
   - JWT algorithm and expiration settings

2. JWT verification utilities
   - verify_jwt_token() to decode and validate
   - get_user_id_from_token() to extract user ID
   - get_user_email_from_token() to extract email

3. Authentication dependencies
   - get_current_user_id() - extracts user ID from token
   - get_current_user() - fetches User from database
   - get_optional_user() - for endpoints that work with/without auth
   - HTTPBearer security scheme

4. Protected endpoint examples
   - /users/me endpoint requiring authentication
   - Resource ownership enforcement (posts)
   - Optional authentication for public/private content

5. CORS configuration
   - Allow specific origins (localhost:3000, production domain)
   - Enable credentials for cookies

**Error Handling**:
- Frontend: AuthenticationError and AuthorizationError classes
- Backend: Consistent HTTP exception handling
- 401 for authentication failures
- 403 for authorization failures

**Security Best Practices**:
- Secret management (32+ chars, environment variables, rotation)
- Token security (HTTPS, expiration, httpOnly cookies, no logging)
- Authorization (verify identity, enforce ownership, proper status codes)
- CORS configuration (exact origins, credentials, restricted methods)

**Testing**:
- Frontend: Mock JWT token attachment
- Backend: Test protected endpoints with/without tokens, expired tokens

The skill provides complete integration between Next.js Better Auth and FastAPI using stateless JWT authentication with proper security, error handling, and authorization enforcement.

## Outcome

- ✅ Impact: Created production-ready JWT & Better Auth integration skill bridging Next.js frontend with FastAPI backend using stateless JWT authentication
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/jwt-better-auth-integration.md (30K)
- 🔁 Next prompts: User may request implementation of authentication system, additional auth features (refresh tokens, role-based access), or move to other project areas
- 🧠 Reflection: This skill fills a critical gap in the full-stack development toolkit by providing secure authentication integration between Next.js and FastAPI. It complements the existing FastAPI skills (routing, validation, security, testing) and enables building authenticated full-stack applications with proper token management, authorization enforcement, and error handling.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
