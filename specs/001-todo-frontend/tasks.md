# Tasks: Todo Web Application Frontend

**Input**: Design documents from `/specs/001-todo-frontend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded from this task list.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: All code in `frontend/` directory
- **Next.js App Router**: `frontend/src/app/` for pages
- **Components**: `frontend/src/components/`
- **Utilities**: `frontend/src/lib/`, `frontend/src/hooks/`, `frontend/src/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize Next.js 14+ project with TypeScript in frontend/ directory
- [x] T002 [P] Install and configure Tailwind CSS in frontend/tailwind.config.js
- [x] T003 [P] Install and configure shadcn/ui components in frontend/
- [x] T004 [P] Install TanStack React Query in frontend/package.json
- [x] T005 [P] Install Better Auth dependencies in frontend/package.json
- [x] T006 [P] Configure ESLint and Prettier in frontend/.eslintrc.json and frontend/.prettierrc
- [x] T007 [P] Create TypeScript configuration in frontend/tsconfig.json with strict mode
- [x] T008 Create environment variables template in frontend/.env.example
- [x] T009 [P] Create global styles in frontend/src/styles/globals.css
- [x] T010 [P] Create utility functions in frontend/src/lib/utils.ts (cn helper for Tailwind)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T011 Create root layout in frontend/src/app/layout.tsx with React Query provider
- [x] T012 Create landing page in frontend/src/app/page.tsx
- [x] T013 [P] Create TypeScript types for User in frontend/src/types/auth.ts
- [x] T014 [P] Create TypeScript types for Task in frontend/src/types/task.ts
- [x] T015 [P] Create TypeScript types for API responses in frontend/src/types/api.ts
- [x] T016 Create API client base in frontend/src/lib/api/client.ts with JWT token handling
- [x] T017 Create Better Auth client configuration in frontend/src/lib/auth/client.ts
- [x] T018 [P] Create useAuth hook in frontend/src/hooks/useAuth.ts
- [x] T019 [P] Create useApiQuery hook in frontend/src/hooks/useApiQuery.ts
- [x] T020 [P] Create useApiMutation hook in frontend/src/hooks/useApiMutation.ts
- [x] T021 [P] Create base UI components: Button in frontend/src/components/ui/button.tsx
- [x] T022 [P] Create base UI components: Input in frontend/src/components/ui/input.tsx
- [x] T023 [P] Create base UI components: Card in frontend/src/components/ui/card.tsx
- [x] T024 [P] Create base UI components: Checkbox in frontend/src/components/ui/checkbox.tsx
- [x] T025 [P] Create base UI components: Modal in frontend/src/components/ui/modal.tsx
- [x] T026 [P] Create base UI components: Form in frontend/src/components/ui/form.tsx
- [x] T027 Create route groups structure: (auth) in frontend/src/app/(auth)/
- [x] T028 Create route groups structure: (dashboard) in frontend/src/app/(dashboard)/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in, and log out to access their personal todo list

**Independent Test**: Create account → log in → see dashboard → log out → redirected to login

### Implementation for User Story 1

- [x] T029 [P] [US1] Create login page in frontend/src/app/(auth)/login/page.tsx
- [x] T030 [P] [US1] Create signup page in frontend/src/app/(auth)/signup/page.tsx
- [x] T031 [P] [US1] Create LoginForm component in frontend/src/components/auth/LoginForm.tsx with email/password validation
- [x] T032 [P] [US1] Create SignupForm component in frontend/src/components/auth/SignupForm.tsx with email/password/name validation
- [x] T033 [US1] Implement useSignIn hook in frontend/src/hooks/useSignIn.ts with Better Auth integration
- [x] T034 [US1] Implement useSignUp hook in frontend/src/hooks/useSignUp.ts with Better Auth integration
- [x] T035 [US1] Implement useSignOut hook in frontend/src/hooks/useSignOut.ts with Better Auth integration
- [x] T036 [US1] Create ProtectedRoute component in frontend/src/components/auth/ProtectedRoute.tsx for dashboard protection
- [x] T037 [US1] Create dashboard layout in frontend/src/app/(dashboard)/layout.tsx with auth check and header
- [x] T038 [US1] Add form validation with Zod schemas in frontend/src/lib/validation/auth.ts
- [x] T039 [US1] Add error handling for authentication failures in login/signup forms
- [x] T040 [US1] Add loading states for authentication operations
- [x] T041 [US1] Implement redirect logic: unauthenticated → login, authenticated → dashboard

**Checkpoint**: At this point, User Story 1 should be fully functional - users can sign up, log in, and log out

---

## Phase 4: User Story 2 - Create and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable authenticated users to create new tasks and view their task list

**Independent Test**: Log in → create several tasks → verify they appear in task list → log out and log back in → tasks still visible

### Implementation for User Story 2

- [x] T042 [US2] Create dashboard page in frontend/src/app/(dashboard)/page.tsx with task list
- [x] T043 [P] [US2] Create TaskList component in frontend/src/components/tasks/TaskList.tsx
- [x] T044 [P] [US2] Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [x] T045 [P] [US2] Create CreateTaskForm component in frontend/src/components/tasks/CreateTaskForm.tsx
- [x] T046 [P] [US2] Create EmptyState component in frontend/src/components/tasks/EmptyState.tsx
- [x] T047 [US2] Implement useTasks hook in frontend/src/hooks/useTasks.ts with React Query
- [x] T048 [US2] Implement useCreateTask mutation hook in frontend/src/hooks/useCreateTask.ts
- [x] T049 [US2] Add task creation API integration in frontend/src/lib/api/tasks.ts
- [x] T050 [US2] Add form validation with Zod schema in frontend/src/lib/validation/task.ts
- [x] T051 [US2] Add loading states for task list fetching
- [x] T052 [US2] Add error handling for task creation failures
- [x] T053 [US2] Add optimistic updates for task creation (instant UI feedback)
- [x] T054 [US2] Implement empty state when user has no tasks

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can authenticate and manage their task list

---

## Phase 5: User Story 3 - Mark Tasks as Complete (Priority: P2)

**Goal**: Enable users to mark tasks as complete to track progress

**Independent Test**: Create tasks → mark some as complete → verify visual distinction → toggle back to incomplete

### Implementation for User Story 3

- [x] T055 [US3] Add checkbox to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [x] T056 [US3] Implement useToggleTaskComplete mutation hook in frontend/src/hooks/useToggleTaskComplete.ts
- [x] T057 [US3] Add task completion API integration in frontend/src/lib/api/tasks.ts
- [x] T058 [US3] Add visual styling for completed tasks (strikethrough, gray text) in TaskItem component
- [x] T059 [US3] Add optimistic updates for task completion toggle (instant UI feedback)
- [x] T060 [US3] Add error handling for completion toggle failures with rollback
- [x] T061 [US3] Add loading state during completion toggle

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently - users can track task completion

---

## Phase 6: User Story 4 - Edit and Delete Tasks (Priority: P2)

**Goal**: Enable users to edit task titles and delete tasks they no longer need

**Independent Test**: Create task → edit title → verify updated → delete task → verify removed from list

### Implementation for User Story 4

- [x] T062 [P] [US4] Create EditTaskModal component in frontend/src/components/tasks/EditTaskModal.tsx
- [x] T063 [P] [US4] Create DeleteConfirmDialog component in frontend/src/components/tasks/DeleteConfirmDialog.tsx
- [x] T064 [US4] Add edit and delete buttons to TaskItem component in frontend/src/components/tasks/TaskItem.tsx
- [x] T065 [US4] Implement useUpdateTask mutation hook in frontend/src/hooks/useUpdateTask.ts
- [x] T066 [US4] Implement useDeleteTask mutation hook in frontend/src/hooks/useDeleteTask.ts
- [x] T067 [US4] Add task update API integration in frontend/src/lib/api/tasks.ts
- [x] T068 [US4] Add task delete API integration in frontend/src/lib/api/tasks.ts
- [x] T069 [US4] Add form validation for edit task modal with Zod schema
- [x] T070 [US4] Add confirmation dialog before task deletion
- [x] T071 [US4] Add optimistic updates for task edit and delete operations
- [x] T072 [US4] Add error handling for edit and delete failures with rollback
- [x] T073 [US4] Add cancel functionality for edit modal

**Checkpoint**: At this point, User Stories 1-4 should all work independently - users have full CRUD capabilities

---

## Phase 7: User Story 5 - Filter and Search Tasks (Priority: P3)

**Goal**: Enable users to filter tasks by status and search by title for quick task discovery

**Independent Test**: Create multiple tasks with different statuses → apply filters → verify correct subset shown → search by title → verify matching tasks displayed

### Implementation for User Story 5

- [x] T074 [P] [US5] Create TaskFilter component in frontend/src/components/tasks/TaskFilter.tsx with All/Active/Completed buttons
- [x] T075 [P] [US5] Create TaskSearch component in frontend/src/components/tasks/TaskSearch.tsx with search input
- [x] T076 [US5] Create TaskFilterContext in frontend/src/contexts/TaskFilterContext.tsx for filter and search state
- [x] T077 [US5] Implement useTaskFilter hook in frontend/src/hooks/useTaskFilter.ts
- [x] T078 [US5] Implement useFilteredTasks hook in frontend/src/hooks/useFilteredTasks.ts with memoization
- [x] T079 [US5] Add filter buttons to dashboard page in frontend/src/app/(dashboard)/page.tsx
- [x] T080 [US5] Add search input to dashboard page in frontend/src/app/(dashboard)/page.tsx
- [x] T081 [US5] Implement debounced search with 300ms delay
- [x] T082 [US5] Add visual feedback for active filter state
- [x] T083 [US5] Add clear filter functionality
- [x] T084 [US5] Update TaskList component to use filtered tasks from useFilteredTasks hook

**Checkpoint**: All user stories should now be independently functional - users can filter and search their tasks

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [x] T085 [P] Add responsive design breakpoints for mobile (375px), tablet (768px), desktop (1024px+)
- [x] T086 [P] Add smooth animations for task operations (add, complete, delete) using Tailwind transitions
- [x] T087 [P] Implement skeleton loading states for task list in frontend/src/components/tasks/TaskListSkeleton.tsx
- [x] T088 [P] Add toast notifications for success/error messages in frontend/src/components/ui/toast.tsx
- [x] T089 [P] Implement keyboard navigation support (Tab, Enter, Escape)
- [x] T090 [P] Add focus management for modals and forms
- [x] T091 [P] Add ARIA labels for accessibility in all interactive components
- [x] T092 [P] Optimize bundle size with code splitting and lazy loading
- [x] T093 [P] Add error boundary component in frontend/src/components/ErrorBoundary.tsx
- [x] T094 [P] Create Header component in frontend/src/components/layout/Header.tsx with user info and logout
- [x] T095 [P] Create Navigation component in frontend/src/components/layout/Navigation.tsx
- [x] T096 [P] Add task statistics display (total, active, completed) in dashboard header
- [x] T097 Implement session expiration handling with redirect to login
- [x] T098 Add network error handling with retry functionality
- [x] T099 Verify all success criteria from spec.md are met (SC-001 to SC-010)
- [x] T100 Run accessibility audit with axe-core and fix issues
- [x] T101 Run Lighthouse performance audit and optimize to score >90
- [x] T102 Test cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- [x] T103 Test mobile responsiveness on iOS Safari and Android Chrome
- [x] T104 Validate quickstart.md setup instructions work correctly
- [x] T105 Create frontend README.md with setup and development instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Requires US1 for authentication but independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Requires US2 for task list but independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Requires US2 for task list but independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Requires US2 for task list but independently testable

### Within Each User Story

- Components can be built in parallel (marked with [P])
- Hooks depend on API client and types (from Foundational phase)
- Forms depend on validation schemas
- Integration tasks depend on component and hook completion
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Components within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all components for User Story 1 together:
Task: "Create login page in frontend/src/app/(auth)/login/page.tsx"
Task: "Create signup page in frontend/src/app/(auth)/signup/page.tsx"
Task: "Create LoginForm component in frontend/src/components/auth/LoginForm.tsx"
Task: "Create SignupForm component in frontend/src/components/auth/SignupForm.tsx"
```

## Parallel Example: User Story 2

```bash
# Launch all components for User Story 2 together:
Task: "Create TaskList component in frontend/src/components/tasks/TaskList.tsx"
Task: "Create TaskItem component in frontend/src/components/tasks/TaskItem.tsx"
Task: "Create CreateTaskForm component in frontend/src/components/tasks/CreateTaskForm.tsx"
Task: "Create EmptyState component in frontend/src/components/tasks/EmptyState.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Authentication)
4. Complete Phase 4: User Story 2 (Create and View Tasks)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

**MVP Scope**: Authentication + Task Creation/Viewing = Functional todo app

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (Auth working!)
3. Add User Story 2 → Test independently → Deploy/Demo (MVP - full task management!)
4. Add User Story 3 → Test independently → Deploy/Demo (Task completion tracking!)
5. Add User Story 4 → Test independently → Deploy/Demo (Full CRUD!)
6. Add User Story 5 → Test independently → Deploy/Demo (Advanced filtering!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Authentication)
   - Developer B: User Story 2 (Task CRUD) - starts after US1 auth is available
   - Developer C: User Story 3 (Task Completion)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All code lives in frontend/ directory with Next.js App Router structure
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests are NOT included as they were not explicitly requested in the specification
- Focus on user value delivery with each story completion
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
