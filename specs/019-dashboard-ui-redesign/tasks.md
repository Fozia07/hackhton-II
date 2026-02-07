# Tasks: Dashboard UI Redesign

**Input**: Design documents from `/specs/019-dashboard-ui-redesign/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted per template guidelines.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `phaseII/frontend/src/` for all frontend changes
- No backend changes required for this feature

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configure dashboard UI components and styling that all user stories depend on

- [X] T001 Create dashboard components directory in phaseII/frontend/src/components/dashboard/
- [ ] T002 [P] Update Tailwind config with dashboard-specific styling in phaseII/frontend/tailwind.config.js
- [ ] T003 [P] Create dashboard styling utilities in phaseII/frontend/src/styles/dashboard.css
- [ ] T004 [P] Create dashboard context for UI state management in phaseII/frontend/src/contexts/DashboardContext.tsx

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update base UI components that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Update existing Todo components to accommodate new UI in phaseII/frontend/src/components/todo/
- [X] T006 [P] Create reusable Tab component with accessibility features in phaseII/frontend/src/components/ui/Tab.tsx
- [X] T007 [P] Create reusable Button variants for dashboard actions in phaseII/frontend/src/components/ui/button.tsx
- [X] T008 Create responsive layout utilities in phaseII/frontend/src/lib/responsive.ts
- [X] T009 Update global styles for dashboard consistency in phaseII/frontend/src/app/globals.css

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Manage Tasks (Priority: P1) 🎯 MVP

**Goal**: Replace the current dashboard UI with new design while preserving all existing functionality - users can see their tasks organized by status (Today, Pending, Overdue) and perform all CRUD operations on tasks with cleaner, more intuitive interface.

**Independent Test**: Load dashboard page and verify new UI layout, all task operations (add, update, delete, complete) work identically to before, backend connections remain unchanged, responsive design works across devices.

### Implementation for User Story 1

- [X] T010 [P] [US1] Create TabNavigation component with Today/Pending/Overdue tabs in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T011 [P] [US1] Create TaskItem component with title, description, and action controls in phaseII/frontend/src/components/dashboard/TaskItem.tsx
- [X] T012 [P] [US1] Create TaskList component that handles filtering by tab status in phaseII/frontend/src/components/dashboard/TaskList.tsx
- [X] T013 [US1] Update dashboard page layout with new header and task section in phaseII/frontend/src/app/dashboard/page.tsx
- [X] T014 [US1] Implement "+ Add Task" button positioning and styling in phaseII/frontend/src/app/dashboard/page.tsx
- [X] T015 [US1] Connect new UI components to existing TodoContext functionality in phaseII/frontend/src/app/dashboard/page.tsx
- [X] T016 [US1] Implement tab filtering logic that integrates with existing filter system in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T017 [US1] Add hover effects and visual feedback for interactive elements in phaseII/frontend/src/components/dashboard/TaskItem.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - users can navigate between tabs, see filtered tasks, and perform all CRUD operations with the new UI

---

## Phase 4: User Story 2 - Navigate Task Status Categories (Priority: P2)

**Goal**: Implement clear visual indication of currently selected tab with smooth transitions between different task status views (Today, Pending, Overdue).

**Independent Test**: Click on different tabs and verify active tab is visually highlighted, task list updates appropriately, transition animations are smooth, and visual design matches reference screenshot.

### Implementation for User Story 2

- [X] T018 [P] [US2] Enhance TabNavigation with active tab highlighting in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T019 [P] [US2] Implement tab transition animations in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T020 [US2] Add visual feedback for tab hover states in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T021 [US2] Update tab filtering to match existing functionality exactly in phaseII/frontend/src/components/dashboard/TaskList.tsx
- [X] T022 [US2] Verify tab accessibility with keyboard navigation in phaseII/frontend/src/components/dashboard/TabNavigation.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - dashboard has new UI with proper tab navigation and filtering

---

## Phase 5: User Story 3 - Responsive Dashboard Experience (Priority: P3)

**Goal**: Ensure dashboard UI works seamlessly across different device sizes, maintaining usability and visual appeal on both desktop and mobile devices.

**Independent Test**: Resize browser window and verify layout adapts appropriately, all interactive elements remain accessible on mobile, touch targets are appropriately sized, and UI remains functional across breakpoints.

### Implementation for User Story 3

- [X] T023 [P] [US3] Implement responsive grid layout for task items in phaseII/frontend/src/components/dashboard/TaskList.tsx
- [X] T024 [P] [US3] Add mobile-specific styling for tab navigation in phaseII/frontend/src/components/dashboard/TabNavigation.tsx
- [X] T025 [US3] Optimize touch targets for mobile devices in phaseII/frontend/src/components/dashboard/TaskItem.tsx
- [X] T026 [US3] Implement responsive header layout in phaseII/frontend/src/app/dashboard/page.tsx
- [X] T027 [US3] Test and adjust layout on common screen sizes (mobile, tablet, desktop) in phaseII/frontend/src/app/dashboard/page.tsx

**Checkpoint**: All user stories should now be independently functional with responsive design

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [X] T028 [P] Update dashboard documentation in phaseII/frontend/README.md
- [X] T029 [P] Validate visual design matches reference screenshot (95% accuracy)
- [X] T030 [P] Test all functionality on multiple browsers (Chrome, Firefox, Safari)
- [X] T031 [P] Verify all interactive elements have proper hover and focus states
- [X] T032 [P] Optimize performance and ensure no regressions in task operations
- [X] T033 [P] Validate accessibility compliance (keyboard navigation, screen readers)
- [X] T034 [P] Run quickstart.md validation steps
- [X] T035 Code cleanup and remove unused styles in phaseII/frontend/src/app/globals.css

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 components
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses US1/US2 components

### Within Each User Story

- Tasks marked [P] can run in parallel (different files)
- Tasks without [P] may have dependencies on previous tasks in same story
- Complete story before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T002-T004)
- All Foundational tasks marked [P] can run in parallel (T006-T007)
- Once Foundational phase completes, User Stories 1, 2, and 3 can start in parallel
- Within each story, tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all parallel tasks for User Story 1 together:
Task: "Create TabNavigation component with Today/Pending/Overdue tabs in phaseII/frontend/src/components/dashboard/TabNavigation.tsx"
Task: "Create TaskItem component with title, description, and action controls in phaseII/frontend/src/components/dashboard/TaskItem.tsx"
Task: "Create TaskList component that handles filtering by tab status in phaseII/frontend/src/components/dashboard/TaskList.tsx"
```

---

## Parallel Example: User Story 2

```bash
# Launch all parallel tasks for User Story 2 together:
Task: "Enhance TabNavigation with active tab highlighting in phaseII/frontend/src/components/dashboard/TabNavigation.tsx"
Task: "Implement tab transition animations in phaseII/frontend/src/components/dashboard/TabNavigation.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T010-T017)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready - MVP with new dashboard UI and all functionality

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready (T001-T009)
2. Add User Story 1 → Test independently → Deploy/Demo (New dashboard UI MVP)
3. Add User Story 2 → Test independently → Deploy/Demo (Enhanced tab navigation)
4. Add User Story 3 → Test independently → Deploy/Demo (Responsive design)
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done:
   - Developer A: User Story 1 (T010-T017)
   - Developer B: User Story 2 (T018-T022)
   - Developer C: User Story 3 (T023-T027)
3. Stories complete and integrate independently
4. Developer D works on Polish phase (T028-T035) in parallel

---

## Task Summary

**Total Tasks**: 35
- **Setup (Phase 1)**: 4 tasks
- **Foundational (Phase 2)**: 5 tasks (BLOCKING)
- **User Story 1 (P1)**: 8 tasks
- **User Story 2 (P2)**: 5 tasks
- **User Story 3 (P3)**: 5 tasks
- **Polish (Phase 6)**: 8 tasks

**Parallel Opportunities**: 19 tasks marked [P] can run in parallel within their phase

**Independent Test Criteria**:
- US1: New dashboard UI loads with all task operations working identically
- US2: Tab navigation works with clear visual indication of active tab
- US3: Dashboard is responsive and usable on mobile and desktop devices

**Suggested MVP Scope**: User Story 1 (New dashboard UI with all functionality) = 8 implementation tasks after foundation

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All tasks follow strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
- Focus on visual enhancements only - no backend changes required
- Maintain existing functionality while adding new UI