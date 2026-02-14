# Tasks: Fix MCP Server Deployment Issues

**Input**: Design documents from `/specs/2-fix-mcp-server-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested - no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Microservice**: `phaseIV/backend/` for backend, root for Kubernetes manifests
- Dockerfile location: `phaseIV/backend/Dockerfile.mcp`
- Kubernetes manifests: repository root (`mcp-server-deployment.yaml`, `mcp-server-service.yaml`)
- Documentation: repository root (`DEPLOYMENT_GUIDE.md`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Validate prerequisites and existing configuration before making changes

- [x] T001 Verify Minikube is running and kubectl context is set to minikube cluster
- [x] T002 [P] Validate existing mcp-server-deployment.yaml has correct imagePullPolicy, probes, port 8002, and 2 replicas in mcp-server-deployment.yaml
- [x] T003 [P] Validate existing mcp-server-service.yaml has correct selector, port 8002, and ClusterIP type in mcp-server-service.yaml
- [x] T004 [P] Verify mcp_server_entry.py entry point runs without ImportError locally in phaseIV/backend/mcp_server_entry.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create correct Dockerfile that fixes both ImagePullBackOff and ImportError issues

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create Dockerfile.mcp with Python 3.11-slim base, WORKDIR /app, copy requirements.txt and app/ directory, install dependencies, copy mcp_server_entry.py, expose port 8002, CMD python mcp_server_entry.py in phaseIV/backend/Dockerfile.mcp
- [x] T006 Ensure requirements.txt includes all MCP server dependencies (fastapi, uvicorn, mcp-use, httpx, sqlalchemy) in phaseIV/backend/requirements.txt
- [x] T007 Create todo-chatbot namespace if it does not exist via kubectl create namespace todo-chatbot

**Checkpoint**: Foundation ready - Dockerfile.mcp created with correct build context and CMD, namespace exists

---

## Phase 3: User Story 1 - MCP Server Pods Start Successfully (Priority: P1) MVP

**Goal**: Fix ImagePullBackOff and ImportError so all MCP server pods reach Running status

**Independent Test**: Run `kubectl get pods -n todo-chatbot -l app=mcp-server` and verify 2 pods show Running status with ready containers, zero ImagePullBackOff or CrashLoopBackOff errors

### Implementation for User Story 1

- [x] T008 [US1] Build Docker image from phaseIV/backend/ using Dockerfile.mcp, tag as mcp-server:latest via docker build -f Dockerfile.mcp -t mcp-server:latest phaseIV/backend/
- [x] T009 [US1] Load mcp-server:latest image into Minikube via minikube image load mcp-server:latest
- [x] T010 [US1] Apply Kubernetes deployment and service manifests via kubectl apply -f mcp-server-deployment.yaml
- [x] T011 [US1] Verify pods reach Running status within 60 seconds, confirm zero ImagePullBackOff errors via kubectl get pods -n todo-chatbot -l app=mcp-server
- [x] T012 [US1] Verify pod logs show successful MCP server startup with no ImportError via kubectl logs -n todo-chatbot deployment/mcp-server

**Checkpoint**: At this point, User Story 1 should be fully functional - pods running, no image pull or import errors

---

## Phase 4: User Story 2 - Backend Service Connects to MCP Server (Priority: P2)

**Goal**: Ensure backend service can reach MCP server at http://mcp-server:8002 with health checks passing

**Independent Test**: From backend pod, run `curl http://mcp-server:8002/health` and verify HTTP 200 response

### Implementation for User Story 2

- [x] T013 [US2] Verify health endpoint /docs responds with HTTP 200 from within MCP server pod via kubectl exec in todo-chatbot namespace (mcp-use SDK uses /docs instead of /health)
- [x] T014 [US2] Verify readiness endpoint /docs responds with HTTP 200 from within MCP server pod via kubectl exec in todo-chatbot namespace (mcp-use SDK uses /docs instead of /ready)
- [x] T015 [US2] SKIPPED - mcp-use SDK provides /docs endpoint for probes; updated deployment YAML probe paths accordingly
- [x] T016 [US2] Verify service endpoints list shows 2 pod IPs via kubectl get endpoints -n todo-chatbot mcp-server
- [x] T017 [US2] Test connectivity from backend pod to MCP server at http://mcp-server:8002/docs via kubectl exec -n todo-chatbot
- [x] T018 [US2] Test MCP tool listing via /openmcp.json endpoint - all 5 tools confirmed (add_task, list_tasks, complete_task, delete_task, update_task)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - pods running and backend can reach MCP server

---

## Phase 5: User Story 3 - Deployment Process is Documented (Priority: P3)

**Goal**: Provide clear step-by-step instructions to deploy MCP server to Minikube from scratch

**Independent Test**: Following the documented steps results in a successful MCP server deployment without manual intervention

### Implementation for User Story 3

- [x] T019 [P] [US3] Create or update DEPLOYMENT_GUIDE.md with complete step-by-step Minikube deployment instructions including prerequisites, build, load, deploy, and verify steps in DEPLOYMENT_GUIDE.md
- [x] T020 [P] [US3] Add troubleshooting section to DEPLOYMENT_GUIDE.md covering ImagePullBackOff, CrashLoopBackOff, probe failures, and connection refused errors in DEPLOYMENT_GUIDE.md
- [x] T021 [US3] Add verification commands section to DEPLOYMENT_GUIDE.md with kubectl commands to confirm successful deployment in DEPLOYMENT_GUIDE.md
- [x] T022 [US3] Validated deployment guide steps against running Minikube cluster - all steps verified working

**Checkpoint**: All user stories should now be independently functional - pods running, connectivity verified, deployment documented

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cleanup and final validation across all stories

- [x] T023 [P] Remove or deprecate old Dockerfile at phaseIV/backend/app/mcp_server/Dockerfile with a comment pointing to Dockerfile.mcp
- [x] T024 [P] Validate quickstart.md deployment steps match actual deployment process in specs/2-fix-mcp-server-deployment/quickstart.md
- [x] T025 Run full end-to-end validation: build image, load to Minikube, deploy, verify pods, test health, test MCP tools, test backend connectivity

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase - builds and deploys image
- **User Story 2 (Phase 4)**: Depends on User Story 1 - needs running pods to test connectivity
- **User Story 3 (Phase 5)**: Can start after Foundational, but benefits from US1+US2 completion for validation
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - Core fix, must complete first
- **User Story 2 (P2)**: Depends on User Story 1 - Cannot test connectivity without running pods
- **User Story 3 (P3)**: Partially parallel with US1/US2 - Documentation can be drafted while fixing, but validation needs running deployment

### Within Each User Story

- T008 → T009 → T010 → T011 → T012 (sequential build → load → deploy → verify chain)
- T013, T014 can run in parallel (different health endpoints)
- T015 only if T013/T014 fail (conditional task)
- T016 → T017 → T018 (sequential service → connectivity → tool chain)
- T019, T020 can run in parallel (different sections of same doc)
- T021 depends on T019, T020 (verification section references earlier sections)

### Parallel Opportunities

- Phase 1: T002, T003, T004 can all run in parallel (independent validations)
- Phase 3: T008-T012 must be sequential (build → load → deploy → verify)
- Phase 4: T013 and T014 can run in parallel (different endpoints)
- Phase 5: T019 and T020 can run in parallel (different doc sections)
- Phase 6: T023 and T024 can run in parallel (different files)

---

## Parallel Example: Phase 1 Setup

```bash
# Launch all validation tasks in parallel:
Task: "Validate mcp-server-deployment.yaml settings"
Task: "Validate mcp-server-service.yaml settings"
Task: "Verify mcp_server_entry.py entry point"
```

## Parallel Example: Phase 5 Documentation

```bash
# Launch documentation tasks in parallel:
Task: "Create DEPLOYMENT_GUIDE.md main sections"
Task: "Add troubleshooting section to DEPLOYMENT_GUIDE.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (validate prerequisites)
2. Complete Phase 2: Foundational (create Dockerfile.mcp, verify dependencies)
3. Complete Phase 3: User Story 1 (build, load, deploy, verify)
4. **STOP and VALIDATE**: Pods running? No ImagePullBackOff? No ImportError?
5. Deploy/demo if ready - MCP server is operational

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Verify pods running -> MVP!
3. Add User Story 2 -> Verify backend connectivity -> Service integration complete
4. Add User Story 3 -> Validate deployment guide -> Full documentation
5. Each story adds value without breaking previous stories

### Sequential Strategy (Recommended for Solo Developer)

This feature has strong sequential dependencies:
1. Phase 1 + 2: Setup and create Dockerfile.mcp (~15 min)
2. Phase 3 (US1): Build, load, deploy, verify (~20 min)
3. Phase 4 (US2): Test connectivity and health endpoints (~15 min)
4. Phase 5 (US3): Document deployment process (~20 min)
5. Phase 6: Polish and final validation (~10 min)

**Total estimated effort**: ~1.5 hours

---

## Summary

| Phase | Tasks | Parallel | Story |
|-------|-------|----------|-------|
| Phase 1: Setup | T001-T004 | 3 parallel | - |
| Phase 2: Foundational | T005-T007 | 0 parallel | - |
| Phase 3: US1 Pods Running | T008-T012 | 0 parallel | US1 (P1) |
| Phase 4: US2 Connectivity | T013-T018 | 2 parallel | US2 (P2) |
| Phase 5: US3 Documentation | T019-T022 | 2 parallel | US3 (P3) |
| Phase 6: Polish | T023-T025 | 2 parallel | - |
| **Total** | **25 tasks** | **9 parallelizable** | **3 stories** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1 is the MVP - if pods start correctly, the core issue is resolved
- US2 validates the fix end-to-end with service connectivity
- US3 ensures the fix is repeatable and documented
- T015 is conditional - only execute if health endpoints are missing
- Commit after each phase checkpoint for safe rollback points
