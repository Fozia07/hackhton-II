# Tasks: Fix Phase II Authentication 503 Error

**Input**: Design documents from `/specs/001-fix-phaseii-503/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Manual E2E testing for authentication flows (no automated tests requested in specification)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phaseII/backend/` and `phaseII/frontend/`
- Backend: `phaseII/backend/app/` for application code
- Frontend: `phaseII/frontend/src/` for source code

---

## Phase 1: Setup (Verification)

**Purpose**: Verify current state and prepare for fixes

- [ ] T001 Verify backend starts successfully on port 8001 using `uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload` from phaseII/backend/
- [ ] T002 Verify frontend starts successfully on port 3001 using `npm run dev` from phaseII/frontend/
- [ ] T003 [P] Verify database connection by calling GET http://localhost:8001/health
- [ ] T004 [P] Document current frontend API URL configuration in phaseII/frontend/.env.local

---

## Phase 2: Foundational (Critical Configuration Fixes)

**Purpose**: Fix root causes of 503 error - BLOCKS all user stories

**⚠️ CRITICAL**: No user story testing can succeed until this phase is complete

- [X] T005 Fix frontend API URL in phaseII/frontend/.env.local - change NEXT_PUBLIC_API_URL from https://fozi07-todo-full-stack-app.hf.space to http://localhost:8001
- [X] T006 Fix backend CORS configuration in phaseII/backend/app/main.py - replace hardcoded origins list with settings.allowed_origins.split(",")
- [X] T007 Verify ALLOWED_ORIGINS in phaseII/backend/.env includes http://localhost:3001
- [ ] T008 Restart frontend server to apply new environment configuration
- [ ] T009 Restart backend server to apply new CORS configuration
- [ ] T010 Verify frontend can reach backend by checking browser network tab shows requests to http://localhost:8001

**Checkpoint**: Foundation ready - frontend now connects to local backend, CORS allows requests

---

## Phase 3: User Story 1 - Successful User Signup (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts successfully without 503 errors

**Independent Test**: Navigate to http://localhost:3001/signup, enter valid credentials (username: testuser1, email: test1@example.com, password: SecurePass123!), submit form, verify account created and redirected to dashboard

### Implementation for User Story 1

- [ ] T011 [US1] Test signup flow via browser - navigate to http://localhost:3001/signup and create new user account
- [ ] T012 [US1] Verify backend logs show incoming POST /auth/signup request in phaseII/backend/ terminal output
- [ ] T013 [US1] Verify backend returns 201 Created with user data (check browser network tab)
- [ ] T014 [US1] Verify user is redirected to dashboard or login page after successful signup
- [ ] T015 [US1] Test signup validation - submit form with invalid email format and verify 400 error with clear message
- [ ] T016 [US1] Test signup duplicate username - create user with existing username and verify 409 error with "Username already registered"
- [ ] T017 [US1] Test signup duplicate email - create user with existing email and verify 409 error with "Email already registered"
- [ ] T018 [US1] Test signup password validation - submit form with password < 8 characters and verify 400 error

**Checkpoint**: User Story 1 complete - signup flow works end-to-end without 503 errors

---

## Phase 4: User Story 2 - Successful User Signin (Priority: P1)

**Goal**: Enable existing users to authenticate and access their accounts without 503 errors

**Independent Test**: Navigate to http://localhost:3001/login, enter credentials from User Story 1 (username: testuser1, password: SecurePass123!), submit form, verify successful authentication and redirect to dashboard

### Implementation for User Story 2

- [ ] T019 [US2] Test signin flow via browser - navigate to http://localhost:3001/login and sign in with existing user
- [ ] T020 [US2] Verify backend logs show incoming POST /auth/signin request in phaseII/backend/ terminal output
- [ ] T021 [US2] Verify backend returns 200 OK with access_token and user data (check browser network tab)
- [ ] T022 [US2] Verify user is redirected to dashboard after successful signin
- [ ] T023 [US2] Verify JWT token is stored in browser (check localStorage or sessionStorage in browser DevTools)
- [ ] T024 [US2] Test signin with email - sign in using email instead of username and verify success
- [ ] T025 [US2] Test signin with invalid password - enter wrong password and verify 401 error with "Incorrect username or password"
- [ ] T026 [US2] Test signin with non-existent user - enter non-existent username and verify 401 error
- [ ] T027 [US2] Test authenticated request - use token from signin to call GET /auth/me and verify 200 OK with user profile

**Checkpoint**: User Stories 1 AND 2 complete - both signup and signin work independently without 503 errors

---

## Phase 5: User Story 4 - Deployment-Ready Backend (Priority: P1)

**Goal**: Ensure backend is properly configured for deployment with all dependencies documented

**Independent Test**: Start backend in clean virtual environment, install dependencies from requirements.txt, verify backend starts successfully and health check returns 200 OK

### Implementation for User Story 4

- [X] T028 [P] [US4] Create requirements-dev.txt in phaseII/backend/ with development dependencies (pytest==8.0.0, pytest-asyncio==0.23.0, black==24.0.0, ruff==0.2.0)
- [X] T029 [P] [US4] Review and clean requirements.txt in phaseII/backend/ - remove psycopg2-binary (using asyncpg instead)
- [X] T030 [US4] Enhance health check endpoint in phaseII/backend/app/main.py - add actual database connectivity test with SELECT 1 query
- [X] T031 [US4] Add database latency measurement to health check in phaseII/backend/app/main.py
- [X] T032 [US4] Update health check to return 503 status code when database is unavailable in phaseII/backend/app/main.py
- [X] T033 [US4] Add version information to health check response in phaseII/backend/app/main.py (read from settings.app_version)
- [ ] T034 [US4] Test enhanced health check - call GET http://localhost:8001/health and verify response includes database.latency_ms and version
- [X] T035 [P] [US4] Create backend README.md in phaseII/backend/ with setup instructions, environment variables, and deployment guide
- [X] T036 [P] [US4] Create frontend README.md in phaseII/frontend/ with setup instructions, environment variables, and deployment guide
- [X] T037 [US4] Update .env.example files in both backend and frontend with all required variables and descriptions
- [ ] T038 [US4] Test deployment readiness - create new virtual environment, install from requirements.txt, verify backend starts without errors

**Checkpoint**: User Story 4 complete - backend is deployment-ready with documented dependencies and enhanced health check

---

## Phase 6: User Story 3 - Clear Error Communication (Priority: P2)

**Goal**: Improve error handling and logging for better debugging and user experience

**Independent Test**: Simulate various error conditions (backend unavailable, validation errors) and verify users receive clear, actionable error messages

### Implementation for User Story 3

- [X] T039 [US3] Add request logging middleware to phaseII/backend/app/main.py - log method, path, status code, and duration for all requests
- [X] T040 [US3] Configure logging format in phaseII/backend/app/main.py - use format "[timestamp] method path status_code duration_ms"
- [ ] T041 [US3] Test request logging - make signup and signin requests and verify logs show all incoming requests with details
- [ ] T042 [US3] Verify authentication error messages are user-friendly - check that 401 errors show "Incorrect username or password" not technical details
- [ ] T043 [US3] Verify validation error messages are specific - check that 400 errors show field-specific messages like "Invalid email format"
- [ ] T044 [US3] Test error handling when backend is stopped - stop backend, attempt signup, verify frontend shows clear error message (not just 503)
- [ ] T045 [US3] Document common error scenarios and solutions in phaseII/backend/README.md troubleshooting section

**Checkpoint**: User Story 3 complete - all errors are logged and users receive clear, actionable error messages

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates

- [X] T046 [P] Update phaseII/frontend/.env.example with correct NEXT_PUBLIC_API_URL=http://localhost:8001
- [X] T047 [P] Update phaseII/backend/.env.example with correct ALLOWED_ORIGINS including localhost:3001
- [ ] T048 Run complete end-to-end test - signup new user, signin, verify dashboard access, check all logs
- [ ] T049 Verify no 503 errors occur during normal authentication flows
- [ ] T050 [P] Document CORS configuration in phaseII/backend/README.md
- [ ] T051 [P] Document environment variable requirements in both README files
- [ ] T052 Validate quickstart.md instructions - follow setup guide from scratch and verify all steps work
- [ ] T053 Create deployment checklist in phaseII/backend/README.md (environment variables, dependencies, health check)
- [ ] T054 Final verification - test all 4 user stories independently to confirm each works as specified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run in parallel with US1 if different testers)
- **User Story 4 (Phase 5)**: Depends on Foundational phase completion (can run in parallel with US1/US2)
- **User Story 3 (Phase 6)**: Depends on Foundational phase completion (can run in parallel with other stories)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Uses user created in US1 for testing but is independently testable
- **User Story 4 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- **User Story 1**: Sequential testing tasks (T011-T018) - each test builds on previous
- **User Story 2**: Sequential testing tasks (T019-T027) - each test builds on previous
- **User Story 4**: Parallel opportunities for documentation tasks (T028, T029, T035, T036, T037 can run in parallel)
- **User Story 3**: Sequential implementation (T039-T040 before T041-T045)

### Parallel Opportunities

- **Phase 1 Setup**: T003 and T004 can run in parallel
- **Phase 2 Foundational**: T005 and T006 can be done in parallel (different files)
- **Phase 5 User Story 4**: T028, T029, T035, T036, T037 can all run in parallel (different files)
- **Phase 7 Polish**: T046, T047, T050, T051 can run in parallel (different files)
- **Between User Stories**: After Phase 2, US1, US2, US3, and US4 can all be worked on in parallel by different team members

---

## Parallel Example: User Story 4

```bash
# Launch all documentation tasks for User Story 4 together:
Task: "Create requirements-dev.txt in phaseII/backend/"
Task: "Review and clean requirements.txt in phaseII/backend/"
Task: "Create backend README.md in phaseII/backend/"
Task: "Create frontend README.md in phaseII/frontend/"
Task: "Update .env.example files in both backend and frontend"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup (verify current state)
2. Complete Phase 2: Foundational (CRITICAL - fix frontend .env.local and backend CORS)
3. Complete Phase 3: User Story 1 (test signup flow)
4. Complete Phase 4: User Story 2 (test signin flow)
5. **STOP and VALIDATE**: Test both signup and signin independently
6. Deploy/demo if ready - core authentication now works!

### Incremental Delivery

1. Complete Setup + Foundational → 503 error fixed!
2. Add User Story 1 → Test independently → Signup works (MVP!)
3. Add User Story 2 → Test independently → Signin works
4. Add User Story 4 → Test independently → Deployment ready
5. Add User Story 3 → Test independently → Better error handling
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (CRITICAL)
2. Once Foundational is done:
   - Developer A: User Story 1 (signup testing)
   - Developer B: User Story 2 (signin testing)
   - Developer C: User Story 4 (deployment readiness)
   - Developer D: User Story 3 (error communication)
3. Stories complete and integrate independently

---

## Critical Path Analysis

**Blocking Tasks** (must complete before anything else):
- T005: Fix frontend .env.local (CRITICAL - root cause of 503 error)
- T006: Fix backend CORS (CRITICAL - secondary issue)

**High Priority** (P1 user stories):
- T011-T018: User Story 1 (signup)
- T019-T027: User Story 2 (signin)
- T028-T038: User Story 4 (deployment readiness)

**Medium Priority** (P2 user stories):
- T039-T045: User Story 3 (error communication)

**Low Priority** (polish):
- T046-T054: Documentation and final validation

---

## Testing Checklist

Before marking each user story complete, verify:

**User Story 1 (Signup)**:
- [ ] New user can create account via browser
- [ ] Backend logs show incoming request
- [ ] Backend returns 201 Created
- [ ] User is redirected after signup
- [ ] Invalid email shows 400 error
- [ ] Duplicate username shows 409 error
- [ ] Duplicate email shows 409 error
- [ ] Short password shows 400 error

**User Story 2 (Signin)**:
- [ ] Existing user can sign in via browser
- [ ] Backend logs show incoming request
- [ ] Backend returns 200 OK with token
- [ ] User is redirected to dashboard
- [ ] Token is stored in browser
- [ ] Can sign in with email
- [ ] Invalid password shows 401 error
- [ ] Non-existent user shows 401 error
- [ ] Token works for authenticated requests

**User Story 4 (Deployment)**:
- [ ] requirements-dev.txt created
- [ ] requirements.txt cleaned
- [ ] Health check enhanced with DB test
- [ ] Health check shows latency
- [ ] Health check returns 503 when unhealthy
- [ ] Backend README created
- [ ] Frontend README created
- [ ] .env.example files updated
- [ ] Backend starts in clean environment

**User Story 3 (Error Communication)**:
- [ ] Request logging middleware added
- [ ] All requests logged with details
- [ ] Error messages are user-friendly
- [ ] Validation errors are specific
- [ ] Backend unavailable shows clear message
- [ ] Troubleshooting documented

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- This is a configuration fix, not new feature development - most tasks are testing and documentation
- No automated tests requested in specification - all testing is manual E2E
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Root cause: Frontend .env.local points to remote URL instead of localhost:8001
- Secondary issue: Backend CORS hardcoded, doesn't include localhost:3001
- No code changes to authentication logic needed - it's already correct

---

## Task Summary

**Total Tasks**: 54

**By Phase**:
- Phase 1 (Setup): 4 tasks
- Phase 2 (Foundational): 6 tasks (CRITICAL)
- Phase 3 (User Story 1): 8 tasks
- Phase 4 (User Story 2): 9 tasks
- Phase 5 (User Story 4): 11 tasks
- Phase 6 (User Story 3): 7 tasks
- Phase 7 (Polish): 9 tasks

**By User Story**:
- User Story 1 (Signup - P1): 8 tasks
- User Story 2 (Signin - P1): 9 tasks
- User Story 3 (Error Communication - P2): 7 tasks
- User Story 4 (Deployment - P1): 11 tasks
- Setup/Foundational/Polish: 19 tasks

**Parallel Opportunities**: 15 tasks marked [P] can run in parallel

**Independent Test Criteria**:
- US1: Create new account via browser, verify success
- US2: Sign in with existing account, verify dashboard access
- US3: Simulate errors, verify clear messages
- US4: Install in clean environment, verify startup

**Suggested MVP Scope**: User Stories 1 & 2 (signup and signin working without 503 errors)

**Format Validation**: ✅ All tasks follow checklist format with checkbox, ID, optional [P] marker, [Story] label for user story tasks, and file paths in descriptions
