# Tasks: Fix 401 Unauthorized Error in Phase III

## Feature Overview
Fix the 401 Unauthorized error occurring in Phase III when using valid Phase II tokens. The issue stems from the `get_user_id_from_token` function not properly extracting user ID from tokens that have "username", "sub", or "user_id" fields.

## Phase 1: Setup
- [ ] T001 Create project structure per implementation plan

## Phase 2: Foundational Tasks
- [ ] T002 Configure development environment for Phase III backend
- [ ] T003 Verify current authentication flow in Phase III
- [ ] T004 Test with Phase II token to reproduce the 401 error

## Phase 3: [US1] Fix Token User ID Extraction
- [ ] T005 [P] [US1] Update get_user_id_from_token function in phaseIII/backend/app/core/security.py
- [ ] T006 [P] [US1] Add debug logging to show token payload in phaseIII/backend/app/core/security.py
- [ ] T007 [US1] Test token extraction with various field combinations
- [ ] T008 [US1] Verify authentication works with Phase II token containing username field
- [ ] T009 [US1] Verify authentication works with Phase II token containing sub field
- [ ] T010 [US1] Verify authentication works with Phase II token containing user_id field

## Phase 4: [US2] Integrate Fixed Authentication
- [ ] T011 [P] [US2] Restart Phase III server with updated security module
- [ ] T012 [US2] Test API endpoint /api/rehan12/chat with Phase II token
- [ ] T013 [US2] Verify 401 error is resolved
- [ ] T014 [US2] Confirm user ID extraction works properly in deps.py dependency

## Phase 5: [US3] Verification and Testing
- [ ] T015 [US3] Test full authentication flow from Phase II to Phase III
- [ ] T016 [US3] Verify both username and user_id path parameters work
- [ ] T017 [US3] Test with different token structures
- [ ] T018 [US3] Confirm backward compatibility with existing Phase III tokens

## Phase 6: Polish & Cross-Cutting Concerns
- [ ] T019 Update documentation regarding Phase II/III token compatibility
- [ ] T020 Clean up debug logging after verification
- [ ] T021 Final testing of the complete flow

## Dependencies
- US1 must be completed before US2
- US2 must be completed before US3

## Parallel Execution Opportunities
- Tasks T005 and T006 can run in parallel as they modify the same file
- User stories can be tested independently after foundational tasks

## Implementation Strategy
- MVP: Complete US1 to fix the core issue
- Incremental delivery: Add verification and testing in subsequent user stories
- Focus on backward compatibility to ensure existing functionality remains intact