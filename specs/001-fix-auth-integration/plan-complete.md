# Implementation Plan: Fix Frontend-Backend Auth Integration Errors

**Branch**: `001-fix-auth-integration` | **Date**: 2026-01-10 | **Spec**: [specs/001-fix-auth-integration/spec.md](specs/001-fix-auth-integration/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan addresses critical frontend-backend integration issues in a Next.js + FastAPI application with JWT authentication. The implementation focuses on resolving three primary errors: "Failed to fetch" during authentication, dashboard 404 errors after login, and AuthContext import/type errors. Additionally, it ensures all Todo application API endpoints function correctly for authenticated users. The plan incorporates reusable debugging skills and agent-assisted validation to systematically resolve issues.

## Technical Context

**Language/Version**: TypeScript (frontend), Python 3.9+ (backend)
**Primary Dependencies**: NextAPI 14+, FastAPI 0.104+, Neon PostgreSQL
**Storage**: Neon PostgreSQL database
**Testing**: Manual testing and browser console validation
**Target Platform**: Web application (browser-based)
**Project Type**: Full-stack web application (frontend + backend)
**Performance Goals**: <500ms response time for auth operations, <1s for dashboard load
**Constraints**: Minimal changes, no major refactoring, demo-ready within 2 hours
**Scale/Scope**: Single user authentication, individual Todo collections per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Following written specification requirements
- ✅ Incremental Evolution: Building on existing working backend/frontend
- ✅ Code Quality: Maintaining existing code standards during fixes
- ✅ Architecture-First: Using existing Next.js/FastAPI architecture
- ✅ Container-First Deployment: Preserving existing deployment approach

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-auth-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phaseII/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI app with CORS configuration
│   │   ├── routes/
│   │   │   ├── auth.py      # Authentication endpoints
│   │   │   └── todos.py     # Todo endpoints
│   │   └── models/
│   │       └── user.py      # User model
│   └── .env                 # Backend configuration
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── (auth)/      # Login/signup pages
    │   │   ├── (dashboard)/ # Protected dashboard
    │   │   └── layout.tsx   # Root layout
    │   ├── components/
    │   │   ├── auth/
    │   │   │   └── ProtectedRoute.tsx  # Route protection
    │   │   └── layout/
    │   │       └── Header.tsx
    │   ├── contexts/
    │   │   └── AuthContext.tsx  # Authentication state management
    │   ├── lib/
    │   │   ├── auth/
    │   │   │   ├── service.ts    # Auth API service
    │   │   │   └── client.ts     # Auth client wrapper
    │   │   └── todo/
    │   │       └── service.ts    # Todo API service
    │   └── types/
    │       └── auth.ts          # Authentication types
    ├── .env.local             # Frontend configuration
    └── package.json
```

**Structure Decision**: Using the existing web application structure with frontend and backend in separate directories, maintaining the Next.js App Router architecture with route groups for authentication and dashboard sections.

## Phase 2: Implementation Tasks

### Phase 2a: Immediate Fixes (Priority 1)
1. **Fix CORS Configuration**: Update backend to allow frontend origin requests
2. **Fix AuthContext Import**: Verify and correct User type import path
3. **Fix ProtectedRoute Logic**: Update authentication checking to prevent 404 errors

### Phase 2b: Secondary Fixes (Priority 2)
1. **Enhance Error Handling**: Replace generic "Failed to fetch" with specific messages
2. **Verify Todo API Integration**: Ensure all Todo endpoints work with JWT authentication
3. **Token Management**: Improve JWT token storage and validation

### Phase 2c: Validation Tasks
1. **End-to-End Testing**: Complete auth flow from signup to dashboard access
2. **Todo Functionality**: Test all CRUD operations after authentication
3. **Error Scenario Testing**: Verify proper error handling for invalid credentials

### Phase 2d: Skill & Agent Integration
1. **Deploy Reusable Debugging Skill**: Apply the "Full-Stack Auth & Routing Debugger" skill to systematically diagnose issues
2. **Agent-Assisted Validation**: Use Claude Code agents to validate fixes and identify remaining issues
3. **Automated Error Detection**: Leverage debugging skill for comprehensive error detection and resolution

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A] | [No violations identified] | [Constitution requirements met] |