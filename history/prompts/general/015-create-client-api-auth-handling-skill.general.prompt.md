---
id: 015
title: Create Client API Auth Handling Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["client-logic", "api-integration", "auth-handling", "skill-creation", "better-auth", "nextjs", "react-query"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/client-api-auth-handling.md
tests:
  - none (documentation work)
---

## Prompt

now create a skill for Client Logic, API Integration & Auth Handling Skill.

STACK:
- Next.js
- Better Auth
- JWT-secured FastAPI backend

RESPONSIBILITIES:
- Integrate Better Auth on frontend
- Handle signup/signin/logout
- Manage authenticated state
- Attach JWT to every API request
- Centralize API client logic
- Handle loading, error, and success states

RULES:
- No UI styling
- No backend JWT verification
- No database logic
- No hardcoded secrets

## Response snapshot

Created comprehensive Client Logic, API Integration & Auth Handling skill documentation (26K) at `.claude/skills/client-api-auth-handling.md`.

The skill covers:

**Better Auth Client Setup:**
- Installation (better-auth, @tanstack/react-query)
- Auth client creation with createAuthClient
- Exported methods (signIn, signUp, signOut, useSession, getSession)
- Environment variables (NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_API_URL)

**Authentication Flows:**
1. Sign Up Flow - useSignUp hook with loading/error states, router redirect
2. Sign In Flow - useSignIn hook with email/password, error handling
3. Sign Out Flow - useSignOut hook with logout and redirect

**Session Management:**
1. useAuth hook - wraps useSession with user, isAuthenticated, isLoading
2. ProtectedRoute component - redirects unauthenticated users
3. Usage patterns in components

**API Client with JWT:**
1. API client setup with automatic JWT attachment
   - getJWTToken() fetches JWT from Better Auth
   - apiFetch() wrapper with Authorization header
   - Error handling (401 → redirect to login, 403 → access denied)
   - API methods (get, post, put, patch, delete)

2. JWT token endpoint (/api/auth/get-jwt)
   - Validates session
   - Generates JWT with auth.api.signJWT
   - Returns token to client

**API Request Hooks:**
1. useApiQuery hook - wraps React Query useQuery with api.get
2. useApiMutation hook - wraps useMutation with api methods, query invalidation

**Error Handling:**
1. API error types (ApiError, AuthenticationError, AuthorizationError, ValidationError, NotFoundError)
2. ErrorBoundary component for API errors

**Loading States:**
1. Global LoadingProvider with context
2. Suspense boundaries for granular loading

**React Query Setup:**
1. QueryClientProvider configuration
2. Default options (staleTime, retry)
3. Integration in app layout

**Best Practices:**
- Centralized API client (no direct fetch calls)
- Proper error handling with custom error types
- Loading state management
- Automatic token attachment
- Type-safe API calls

The skill provides complete client-side authentication and API integration patterns for Next.js with Better Auth and JWT-secured FastAPI backends.

## Outcome

- ✅ Impact: Created production-ready Client Logic, API Integration & Auth Handling skill with comprehensive Better Auth integration, JWT token management, API client patterns, and React Query hooks
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/client-api-auth-handling.md (26K)
- 🔁 Next prompts: User may request additional frontend skills (data fetching patterns, state management, form handling), implement authentication system, or move to other project areas
- 🧠 Reflection: This skill complements jwt-better-auth-integration.md by focusing on the client-side implementation. Combined with ui-components-design-system.md and nextjs-app-architecture.md, developers now have complete frontend patterns for building authenticated Next.js applications with proper API integration, error handling, and state management.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
