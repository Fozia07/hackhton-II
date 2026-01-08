---
id: 7
title: "Frontend Authentication API Alignment"
stage: "spec"
date: "2026-01-08"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "005-auth-api-alignment"
branch: "005-auth-api-alignment"
user: "Fozia"
command: "/sp.specify Frontend Authentication API Alignment Specification\\nHackathon 2 – Phase II\\nBetter Auth Email/Password Login\\n\\nObjective:\\nClarify and correct the frontend authentication implementation\\nby aligning it with the actual Better Auth client API.\\n\\nThis specification exists because the current implementation\\nassumes a credentials-based signIn API that does not exist.\\n\\nTarget Audience:\\n- Claude Code implementing frontend authentication\\n- Hackathon evaluators reviewing spec-driven corrections\\n- Frontend developers using Better Auth\\n\\nProblem Statement:\\nThe frontend attempts to call `signIn.credentials(...)`,\\nbut TypeScript reports that this method does not exist.\\n\\nThe Better Auth client exposes `signIn.social`,\\nindicating that email/password authentication\\nmust be implemented differently.\\n\\nThis mismatch causes compile-time failures and blocks frontend execution.\\n\\n---\\n\\nFunctional Requirements:\\n\\n1. API Correctness\\n- Frontend must only use authentication methods that exist\\n  in the Better Auth client API\\n- No assumptions about credentials-based APIs are allowed\\n\\n2. Email/Password Authentication\\n- Email/password login must be implemented using\\n  the officially supported Better Auth approach\\n- Implementation must align with Better Auth documentation\\n\\n3. Type Safety\\n- TypeScript must compile without errors\\n- No usage of non-existent properties or methods\\n\\n---\\n\\nAcceptance Criteria:\\n\\n- Frontend compiles successfully\\n- No TypeScript errors related to authentication\\n- Signup and login flows work using supported APIs\\n- No usage of `signIn.credentials`\\n- Authentication implementation matches Better Auth API surface\\n\\n---\\n\\nConstraints:\\n\\n- No backend changes\\n- No custom authentication system\\n- No bypassing TypeScript with `any`\\n- No undocumented APIs\\n\\n---\\n\\nNot Building:\\n\\n- Custom auth logic\\n- Password hashing\\n- Backend auth endpoints\\n- Social login (unless already implemented)\\n\\n---\\n\\nSuccess Criteria:\\n- Authentication code reflects real Better Auth API\\n- Frontend builds successfully\\n- Spec-driven correction is documented"
labels: ["authentication", "api-alignment", "better-auth", "frontend", "typescript"]
links:
  spec: "specs/005-auth-api-alignment/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/005-auth-api-alignment/spec.md"
  - "specs/005-auth-api-alignment/plan.md"
  - "specs/005-auth-api-alignment/tasks.md"
  - "specs/005-auth-api-alignment/checklists/requirements.md"
tests: []
---

# Prompt History Record

## Original Prompt
```
/sp.specify

Frontend Authentication API Alignment Specification
Hackathon 2 – Phase II
Better Auth Email/Password Login

Objective:
Clarify and correct the frontend authentication implementation
by aligning it with the actual Better Auth client API.

This specification exists because the current implementation
assumes a credentials-based signIn API that does not exist.

Target Audience:
- Claude Code implementing frontend authentication
- Hackathon evaluators reviewing spec-driven corrections
- Frontend developers using Better Auth

Problem Statement:
The frontend attempts to call `signIn.credentials(...)`,
but TypeScript reports that this method does not exist.

The Better Auth client exposes `signIn.social`,
indicating that email/password authentication
must be implemented differently.

This mismatch causes compile-time failures and blocks frontend execution.

---

Functional Requirements:

1. API Correctness
- Frontend must only use authentication methods that exist
  in the Better Auth client API
- No assumptions about credentials-based APIs are allowed

2. Email/Password Authentication
- Email/password login must be implemented using
  the officially supported Better Auth approach
- Implementation must align with Better Auth documentation

3. Type Safety
- TypeScript must compile without errors
- No usage of non-existent properties or methods

---

Acceptance Criteria:

- Frontend compiles successfully
- No TypeScript errors related to authentication
- Signup and login flows work using supported APIs
- No usage of `signIn.credentials`
- Authentication implementation matches Better Auth API surface

---

Constraints:

- No backend changes
- No custom authentication system
- No bypassing TypeScript with `any`
- No undocumented APIs

---

Not Building:

- Custom auth logic
- Password hashing
- Backend auth endpoints
- Social login (unless already implemented)

---

Success Criteria:
- Authentication code reflects real Better Auth API
- Frontend builds successfully
- Spec-driven correction is documented
```

## Response Summary
Successfully created a comprehensive specification for aligning the frontend authentication implementation with the actual Better Auth client API. The specification addresses the issue where the frontend was attempting to call non-existent methods like `signIn.credentials(...)` which was causing TypeScript compilation errors.

Created complete spec, plan, and tasks files that document:
- The API alignment problem and its resolution
- Concrete decisions about removing unsupported APIs and using direct method calls
- The client-level redirect configuration approach to fix fetch API errors
- Authentication strategy alignment with server configuration
- Implementation tasks with specific method replacements
- Quality assurance measures to ensure type safety

The specification provides clear guidance for implementing the fix while maintaining constraints of no backend changes, no undocumented APIs, and proper type safety.

## Outcome
Created a complete SDD specification for the frontend authentication API alignment that defines the requirements for correcting the authentication implementation to use only methods that exist in the Better Auth client API. The specification provides clear documentation for the implementation team to follow in subsequent phases, ensuring type safety and proper API usage.