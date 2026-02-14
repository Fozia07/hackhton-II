---
description: "Task list for Local Kubernetes Deployment of Todo AI Chatbot"
---

# Tasks: Local Kubernetes Deployment of Todo AI Chatbot

**Input**: Design documents from `/specs/1-k8s-todo-deployment/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, helm-chart-design.md, contracts/, quickstart.md

**Tests**: No test tasks included - this is infrastructure deployment work focused on Kubernetes resource creation and validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each deployment component.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Helm charts**: `helm-charts/todo-chatbot/`
- **Scripts**: `scripts/`
- **Documentation**: `docs/kubernetes/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and prerequisite verification

- [x] T001 Create Helm chart directory structure at helm-charts/todo-chatbot/
- [x] T002 Verify Minikube cluster is running and accessible via kubectl
- [x] T003 [P] Verify Docker images exist locally (phase4-frontend:latest, phase4-backend:latest)
- [x] T004 [P] Verify Helm 3.x is installed and functional
- [x] T005 [P] Verify Phase II authentication service is accessible at https://fozi07-todo-full-stack-app.hf.space
- [x] T006 Create scripts directory at scripts/ for deployment automation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Helm chart infrastructure that MUST be complete before ANY user story deployment

**⚠️ CRITICAL**: No service deployment can begin until this phase is complete

- [x] T007 Point Docker CLI to Minikube's Docker daemon using eval $(minikube docker-env)
- [x] T008 Verify Docker images are available in Minikube using docker images command
- [x] T009 Create Chart.yaml with metadata at helm-charts/todo-chatbot/Chart.yaml
- [x] T010 Create base values.yaml with global configuration at helm-charts/todo-chatbot/values.yaml
- [x] T011 Create _helpers.tpl with template functions at helm-charts/todo-chatbot/templates/_helpers.tpl
- [x] T012 [P] Create backend template directory at helm-charts/todo-chatbot/templates/backend/
- [x] T013 [P] Create frontend template directory at helm-charts/todo-chatbot/templates/frontend/
- [x] T014 Create NOTES.txt with post-install instructions at helm-charts/todo-chatbot/templates/NOTES.txt
- [x] T015 Create .helmignore file at helm-charts/todo-chatbot/.helmignore

**Checkpoint**: Helm chart structure ready - service deployment can now begin

---

## Phase 3: User Story 1 - Deploy Backend Service with External Authentication (Priority: P1) 🎯 MVP

**Goal**: Deploy backend service to Kubernetes with connectivity to Phase II authentication service on HuggingFace

**Independent Test**: Backend pods start successfully, health checks pass, and authentication requests are forwarded to Phase II service

### Implementation for User Story 1

- [x] T016 [US1] Create backend Deployment template at helm-charts/todo-chatbot/templates/backend/deployment.yaml
- [x] T017 [US1] Configure backend container image and pull policy in deployment template
- [x] T018 [US1] Configure backend environment variables (AUTH_SERVICE_URL, PORT, LOG_LEVEL) in deployment template
- [x] T019 [US1] Configure backend liveness probe (HTTP GET /health, 30s initial delay) in deployment template
- [x] T020 [US1] Configure backend readiness probe (HTTP GET /health, 5s initial delay) in deployment template
- [x] T021 [US1] Configure backend resource requests (100m CPU, 128Mi memory) in deployment template
- [x] T022 [US1] Configure backend resource limits (200m CPU, 256Mi memory) in deployment template
- [x] T023 [US1] Configure backend replica count (default: 2) in deployment template
- [x] T024 [US1] Configure backend rolling update strategy (maxSurge: 1, maxUnavailable: 0) in deployment template
- [x] T025 [US1] Add backend labels and annotations in deployment template
- [x] T026 [US1] Create backend Service template at helm-charts/todo-chatbot/templates/backend/service.yaml
- [x] T027 [US1] Configure backend Service type as ClusterIP in service template
- [x] T028 [US1] Configure backend Service port mapping (80 → 8000) in service template
- [x] T029 [US1] Add backend Service labels and selectors in service template
- [x] T030 [US1] Update values.yaml with backend configuration section
- [x] T031 [US1] Validate Helm chart syntax using helm lint command
- [x] T032 [US1] Perform dry-run deployment using helm install --dry-run --debug
- [x] T033 [US1] Deploy backend service using helm install todo-chatbot command
- [x] T034 [US1] Verify backend pods are created using kubectl get pods -n todo-chatbot
- [x] T035 [US1] Wait for backend pods to reach Running state using kubectl wait command
- [x] T036 [US1] Verify backend pods pass readiness probes using kubectl get pods
- [x] T037 [US1] Check backend pod logs for startup errors using kubectl logs
- [x] T038 [US1] Verify backend Service is created using kubectl get services -n todo-chatbot
- [x] T039 [US1] Verify backend Service has endpoints using kubectl get endpoints -n todo-chatbot
- [x] T040 [US1] Port-forward to backend Service using kubectl port-forward
- [x] T041 [US1] Test backend health endpoint using curl http://localhost:8000/health
- [x] T042 [US1] Test backend authentication flow to Phase II service using curl or API client
- [x] T043 [US1] Verify backend resource usage is within limits using kubectl top pods
- [x] T044 [US1] Document backend deployment validation results

**Checkpoint**: Backend service is fully deployed, healthy, and can authenticate via Phase II service

---

## Phase 4: User Story 2 - Deploy Frontend Service with Backend Connectivity (Priority: P2)

**Goal**: Deploy frontend service to Kubernetes with connectivity to backend service

**Independent Test**: Frontend pods start successfully, UI is accessible from host machine, and frontend can communicate with backend

### Implementation for User Story 2

- [x] T045 [US2] Create frontend Deployment template at helm-charts/todo-chatbot/templates/frontend/deployment.yaml
- [x] T046 [US2] Configure frontend container image and pull policy in deployment template
- [x] T047 [US2] Configure frontend environment variables (BACKEND_URL, PORT) in deployment template with backend service DNS
- [x] T048 [US2] Configure frontend liveness probe (HTTP GET /health, 30s initial delay) in deployment template
- [x] T049 [US2] Configure frontend readiness probe (HTTP GET /health, 5s initial delay) in deployment template
- [x] T050 [US2] Configure frontend resource requests (50m CPU, 64Mi memory) in deployment template
- [x] T051 [US2] Configure frontend resource limits (100m CPU, 128Mi memory) in deployment template
- [x] T052 [US2] Configure frontend replica count (default: 2) in deployment template
- [x] T053 [US2] Configure frontend rolling update strategy (maxSurge: 1, maxUnavailable: 0) in deployment template
- [x] T054 [US2] Add frontend labels and annotations in deployment template
- [x] T055 [US2] Create frontend Service template at helm-charts/todo-chatbot/templates/frontend/service.yaml
- [x] T056 [US2] Configure frontend Service type as NodePort in service template
- [x] T057 [US2] Configure frontend Service port mapping (80 → 3000 → 30080) in service template
- [x] T058 [US2] Add frontend Service labels and selectors in service template
- [x] T059 [US2] Update values.yaml with frontend configuration section
- [x] T060 [US2] Validate updated Helm chart syntax using helm lint command
- [x] T061 [US2] Perform dry-run upgrade using helm upgrade --dry-run --debug
- [x] T062 [US2] Upgrade deployment to include frontend using helm upgrade todo-chatbot command
- [x] T063 [US2] Verify frontend pods are created using kubectl get pods -n todo-chatbot
- [x] T064 [US2] Wait for frontend pods to reach Running state using kubectl wait command
- [x] T065 [US2] Verify frontend pods pass readiness probes using kubectl get pods
- [x] T066 [US2] Check frontend pod logs for startup errors using kubectl logs
- [x] T067 [US2] Verify frontend Service is created using kubectl get services -n todo-chatbot
- [x] T068 [US2] Verify frontend Service has endpoints using kubectl get endpoints -n todo-chatbot
- [x] T069 [US2] Get frontend access URL using minikube service todo-chatbot-frontend command
- [x] T070 [US2] Access frontend in browser and verify UI loads successfully
- [x] T071 [US2] Test frontend-to-backend communication by performing an action in UI
- [x] T072 [US2] Verify frontend can send requests to backend using browser DevTools Network tab
- [x] T073 [US2] Test end-to-end authentication flow (frontend → backend → Phase II auth service)
- [x] T074 [US2] Verify frontend resource usage is within limits using kubectl top pods
- [x] T075 [US2] Document frontend deployment validation results

**Checkpoint**: Frontend service is fully deployed, accessible from host, and communicates with backend

---

## Phase 5: User Story 3 - Configure Service Resilience and Scaling (Priority: P3)

**Goal**: Configure production-grade resilience with resource limits, health checks, and multiple replicas

**Independent Test**: Services survive pod failures, traffic is distributed across replicas, and resource limits are enforced

### Implementation for User Story 3

- [x] T076 [US3] Verify backend replica count is set to 2 in values.yaml
- [x] T077 [US3] Verify frontend replica count is set to 2 in values.yaml
- [x] T078 [US3] Verify all pods are running with 2 replicas each using kubectl get pods
- [x] T079 [US3] Test backend pod failure recovery by deleting one backend pod using kubectl delete pod
- [x] T080 [US3] Verify Kubernetes automatically recreates deleted backend pod using kubectl get pods -w
- [x] T081 [US3] Verify backend Service continues to work during pod recreation
- [x] T082 [US3] Test frontend pod failure recovery by deleting one frontend pod using kubectl delete pod
- [x] T083 [US3] Verify Kubernetes automatically recreates deleted frontend pod using kubectl get pods -w
- [x] T084 [US3] Verify frontend Service continues to work during pod recreation
- [x] T085 [US3] Verify traffic is distributed across backend replicas using kubectl logs on multiple pods
- [x] T086 [US3] Verify traffic is distributed across frontend replicas using kubectl logs on multiple pods
- [x] T087 [US3] Monitor resource usage for all pods using kubectl top pods
- [x] T088 [US3] Verify no pods exceed their CPU limits (backend: 200m, frontend: 100m)
- [x] T089 [US3] Verify no pods exceed their memory limits (backend: 256Mi, frontend: 128Mi)
- [x] T090 [US3] Test liveness probe by simulating unhealthy backend pod (if possible)
- [x] T091 [US3] Verify Kubernetes restarts unhealthy pods automatically
- [x] T092 [US3] Test readiness probe by checking pod removal from Service during startup
- [x] T093 [US3] Verify Service only routes traffic to ready pods
- [x] T094 [US3] Document resilience test results and recovery times

**Checkpoint**: Services demonstrate production-grade resilience with automatic recovery and load distribution

---

## Phase 6: User Story 4 - Manage Configuration Through Helm (Priority: P4)

**Goal**: Enable deployment management through Helm with upgrades, rollbacks, and environment-specific configuration

**Independent Test**: Helm operations (upgrade, rollback) work correctly and configuration changes are applied without downtime

### Implementation for User Story 4

- [x] T095 [US4] Create values-dev.yaml with development environment overrides at helm-charts/todo-chatbot/values-dev.yaml
- [x] T096 [US4] Configure reduced replica counts (1 per service) in values-dev.yaml
- [x] T097 [US4] Configure reduced resource limits for development in values-dev.yaml
- [x] T098 [US4] Test Helm upgrade with configuration change (e.g., increase backend replicas to 3)
- [x] T099 [US4] Execute helm upgrade todo-chatbot command with new replica count
- [x] T100 [US4] Monitor rolling update progress using kubectl rollout status
- [x] T101 [US4] Verify new pods are created with updated configuration
- [x] T102 [US4] Verify zero downtime during upgrade (services remain accessible)
- [x] T103 [US4] Verify upgrade completes within 1 minute per success criteria
- [x] T104 [US4] Check Helm release history using helm history todo-chatbot
- [x] T105 [US4] Test Helm rollback to previous revision using helm rollback todo-chatbot
- [x] T106 [US4] Verify rollback restores previous configuration
- [x] T107 [US4] Verify services remain functional after rollback
- [x] T108 [US4] Test deployment with values-dev.yaml using helm install with -f flag
- [x] T109 [US4] Verify development-specific values are applied correctly
- [x] T110 [US4] Test Helm uninstall and reinstall cycle
- [x] T111 [US4] Verify complete cleanup after uninstall using kubectl get all
- [x] T112 [US4] Verify successful reinstall with all resources recreated
- [x] T113 [US4] Document Helm operational procedures (install, upgrade, rollback, uninstall)

**Checkpoint**: Helm provides full deployment lifecycle management with zero-downtime operations

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Automation, documentation, and operational improvements

- [x] T114 [P] Create load-images.sh script at scripts/load-images.sh for Docker image loading
- [x] T115 [P] Create deploy.sh script at scripts/deploy.sh for automated deployment
- [x] T116 [P] Create validate.sh script at scripts/validate.sh for post-deployment validation
- [x] T117 [P] Create cleanup.sh script at scripts/cleanup.sh for teardown
- [x] T118 [P] Create deployment guide at docs/kubernetes/deployment-guide.md
- [x] T119 [P] Create troubleshooting guide at docs/kubernetes/troubleshooting.md
- [x] T120 [P] Create architecture diagram at docs/kubernetes/architecture.md
- [x] T121 [P] Update README.md with Kubernetes deployment instructions
- [x] T122 Verify all success criteria from spec.md are met
- [x] T123 Run complete end-to-end validation following quickstart.md
- [x] T124 Document any issues encountered and resolutions
- [x] T125 Create deployment checklist for future deployments

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (backend deployment from US1 should be complete for full testing)
- **User Story 3 (Phase 5)**: Depends on US1 and US2 being deployed (tests resilience of existing deployments)
- **User Story 4 (Phase 6)**: Depends on US1 and US2 being deployed (tests Helm operations on existing deployment)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Backend should be deployed for full end-to-end testing
- **User Story 3 (P3)**: Requires US1 and US2 deployed - Tests resilience of existing services
- **User Story 4 (P4)**: Requires US1 and US2 deployed - Tests Helm operations on existing deployment

### Within Each User Story

- **US1 (Backend)**: Template creation → Configuration → Deployment → Validation
- **US2 (Frontend)**: Template creation → Configuration → Deployment → Validation → End-to-end testing
- **US3 (Resilience)**: Verification → Failure testing → Recovery validation
- **US4 (Helm)**: Environment configs → Upgrade testing → Rollback testing → Documentation

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T004, T005 can run in parallel (different verification tasks)
- **Phase 2 (Foundational)**: T012, T013 can run in parallel (different directories)
- **Phase 7 (Polish)**: T114, T115, T116, T117, T118, T119, T120, T121 can all run in parallel (different files)

---

## Parallel Example: Foundational Phase

```bash
# Launch directory creation tasks together:
Task: "Create backend template directory at helm-charts/todo-chatbot/templates/backend/"
Task: "Create frontend template directory at helm-charts/todo-chatbot/templates/frontend/"
```

---

## Parallel Example: Polish Phase

```bash
# Launch all documentation and script tasks together:
Task: "Create load-images.sh script at scripts/load-images.sh"
Task: "Create deploy.sh script at scripts/deploy.sh"
Task: "Create validate.sh script at scripts/validate.sh"
Task: "Create cleanup.sh script at scripts/cleanup.sh"
Task: "Create deployment guide at docs/kubernetes/deployment-guide.md"
Task: "Create troubleshooting guide at docs/kubernetes/troubleshooting.md"
Task: "Create architecture diagram at docs/kubernetes/architecture.md"
Task: "Update README.md with Kubernetes deployment instructions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Backend Deployment)
4. **STOP and VALIDATE**: Test backend independently with Phase II auth
5. Deploy/demo backend service

### Incremental Delivery

1. Complete Setup + Foundational → Helm chart foundation ready
2. Add User Story 1 (Backend) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Frontend) → Test end-to-end → Deploy/Demo (Complete application!)
4. Add User Story 3 (Resilience) → Test failure recovery → Deploy/Demo (Production-ready!)
5. Add User Story 4 (Helm Management) → Test operations → Deploy/Demo (Fully managed!)
6. Each story adds value without breaking previous stories

### Sequential Execution (Recommended for Solo Developer)

1. Phase 1: Setup (verify prerequisites)
2. Phase 2: Foundational (create Helm chart structure)
3. Phase 3: User Story 1 (deploy and validate backend)
4. Phase 4: User Story 2 (deploy and validate frontend)
5. Phase 5: User Story 3 (test resilience)
6. Phase 6: User Story 4 (test Helm operations)
7. Phase 7: Polish (automation and documentation)

---

## Success Criteria Validation

Each user story maps to specific success criteria from spec.md:

### User Story 1 (Backend)
- **SC-001**: Deploy within 2 minutes (validate with T033)
- **SC-002**: Pods ready within 60s (validate with T035)
- **SC-004**: Auth response < 3s (validate with T042)
- **SC-008**: Resources within limits (validate with T043)
- **SC-009**: Probes detect failure < 10s (validate with T019, T020)

### User Story 2 (Frontend)
- **SC-001**: Deploy within 2 minutes (validate with T062)
- **SC-002**: Pods ready within 60s (validate with T064)
- **SC-003**: Frontend accessible within 10s (validate with T070)
- **SC-006**: 10+ concurrent sessions (validate with T073)
- **SC-008**: Resources within limits (validate with T074)

### User Story 3 (Resilience)
- **SC-005**: 99% uptime, 30s recovery (validate with T079-T084)
- **SC-009**: Probes detect failure < 10s (validate with T090-T093)

### User Story 4 (Helm)
- **SC-007**: Helm upgrade < 1 minute (validate with T103)
- **SC-010**: Redeploy within 3 minutes (validate with T110-T112)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No test tasks included - this is infrastructure deployment, validation is done through kubectl commands and manual testing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Use kubernetes-developer skill for all Kubernetes resource creation and configuration (per FR-021)
- All Helm templates must follow best practices from helm-chart-design.md
- All configuration must match contracts in contracts/ directory

---

## Task Count Summary

- **Total Tasks**: 125
- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (US1 - Backend)**: 29 tasks
- **Phase 4 (US2 - Frontend)**: 31 tasks
- **Phase 5 (US3 - Resilience)**: 19 tasks
- **Phase 6 (US4 - Helm Management)**: 19 tasks
- **Phase 7 (Polish)**: 12 tasks

**Parallel Opportunities**: 11 tasks marked [P] can run in parallel within their phases

**MVP Scope**: Phases 1-3 (44 tasks) deliver working backend with authentication

**Full Application**: Phases 1-4 (75 tasks) deliver complete frontend + backend system

**Production Ready**: All phases (125 tasks) deliver fully managed, resilient deployment
