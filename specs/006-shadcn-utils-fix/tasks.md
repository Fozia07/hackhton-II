# Frontend Build Error Resolution for shadcn/ui Utilities (Vercel Deployment) - Implementation Tasks

## Task Overview
Resolve Vercel build-time errors related to missing module resolution for '@/lib/utils' and fix TypeScript compilation errors with 'verbatimModuleSyntax' setting.

## Implementation Tasks

### Phase 1: Setup
- [X] T001 Create tasks file for shadcn/ui utilities fix implementation

### Phase 2: Foundational
- [X] T002 Audit all files with incorrect type imports causing 'verbatimModuleSyntax' errors
- [X] T003 Verify current build process to document baseline errors

### Phase 3: [US1] Fix Type-Only Imports
- [ ] T004 [P] [US1] Update Task type import in src/components/tasks/EditTaskModal.tsx to use 'type' keyword
- [ ] T005 [P] [US1] Update Task type import in src/components/tasks/TaskItem.tsx to use 'type' keyword
- [ ] T006 [P] [US1] Update Task type import in src/components/tasks/TaskList.tsx to use 'type' keyword
- [ ] T007 [P] [US1] Update TaskFilter type import in src/contexts/TaskFilterContext.tsx to use 'type' keyword
- [ ] T008 [P] [US1] Update User type import in src/hooks/useAuth.ts to use 'type' keyword

### Phase 4: [US2] Fix React Component Type Imports
- [ ] T009 [P] [US2] Update ReactNode import in src/components/auth/ProtectedRoute.tsx to use 'type' keyword
- [ ] T010 [P] [US2] Update ReactNode import in src/components/ErrorBoundary.tsx to use 'type' keyword
- [ ] T011 [P] [US2] Update ReactNode import in src/components/providers/ReactQueryClientProvider.tsx to use 'type' keyword
- [ ] T012 [P] [US2] Update ReactNode import in src/contexts/TaskFilterContext.tsx to use 'type' keyword

### Phase 5: [US3] Fix Component API Usage
- [X] T013 [US3] Update checkbox component usage in src/components/tasks/TaskItem.tsx to use 'onChange' instead of 'onCheckedChange'

### Phase 6: [US4] Fix Hook Return Values
- [X] T014 [US4] Update useAuth hook in src/hooks/useAuth.ts to properly handle Better Auth useSession return values

### Phase 7: [US5] Validate Build Process
- [X] T015 [US5] Test build process with 'npm run build' to verify all TypeScript errors are resolved
- [X] T016 [US5] Confirm all shadcn/ui components compile successfully
- [X] T017 [US5] Verify '@/lib/utils' resolves correctly in all shadcn/ui components

### Phase 8: Polish & Cross-Cutting Concerns
- [X] T018 Verify all UI components function correctly after changes
- [X] T019 Test authentication flows to ensure no regression
- [X] T020 Prepare for Vercel deployment with verified build process

## Constraints
- Do not modify backend authentication logic
- Do not remove or replace shadcn/ui components
- Maintain existing folder structure under `src/`
- Comply with Next.js App Router conventions
- Ensure changes are suitable for Vercel deployment

## Dependencies
- Task T002 must complete before T004-T014 (baseline errors needed)
- All user story tasks (T004-T014) must complete before T015 (build validation)

## Parallel Execution Opportunities
- Tasks T004-T008 can be executed in parallel (different files with type import fixes)
- Tasks T009-T012 can be executed in parallel (different files with ReactNode import fixes)

## Implementation Strategy
- Focus on type import fixes first to resolve 'verbatimModuleSyntax' errors
- Update component API usage to match actual component signatures
- Test build process incrementally to catch errors early
- Verify functionality after each change to prevent regressions