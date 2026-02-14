# Implementation Plan: Local Kubernetes Deployment of Todo AI Chatbot

**Branch**: `1-k8s-todo-deployment` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-k8s-todo-deployment/spec.md`

## Summary

Deploy Phase IV Todo AI Chatbot frontend and backend services to local Kubernetes cluster using Helm charts and Minikube. Backend service connects to Phase II authentication service hosted on HuggingFace. Implementation follows production-grade Kubernetes best practices using the kubernetes-developer skill for all cluster configuration, deployment design, and resource management.

**Primary Requirement**: Deploy containerized frontend and backend services with proper health checks, resource limits, multiple replicas, and external authentication integration.

**Technical Approach**: Use Helm charts to package Kubernetes Deployments and Services with templated configuration. Load pre-built Docker images into Minikube, deploy services with production-grade settings (probes, resource limits, replicas), and validate end-to-end functionality including authentication flow through external HuggingFace service.

## Technical Context

**Language/Version**:
- Frontend: JavaScript/TypeScript (Node.js 20 or similar)
- Backend: Python 3.11+ or Node.js 20+ (based on Phase IV implementation)

**Primary Dependencies**:
- Kubernetes 1.28+ (via Minikube)
- Helm 3.x
- Docker (for image management)
- kubectl CLI

**Storage**: N/A (stateless services, no persistent storage required)

**Testing**:
- kubectl commands for pod/service validation
- curl/browser for endpoint testing
- End-to-end authentication flow testing

**Target Platform**: Local Kubernetes cluster (Minikube) on development machine

**Project Type**: Kubernetes deployment (infrastructure-as-code)

**Performance Goals**:
- Pod startup < 60 seconds
- Service response time < 2 seconds (95th percentile)
- Deployment completion < 2 minutes
- Support 10+ concurrent user sessions

**Constraints**:
- Local Minikube resources (4GB RAM, 2 CPUs minimum)
- External dependency on HuggingFace service availability
- Pre-built Docker images (no modification allowed)
- Stateless services only

**Scale/Scope**:
- 2 services (frontend, backend)
- 2-3 replicas per service
- Single Helm chart with multiple sub-charts or unified chart
- Local development environment only

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Spec-Driven Development
- **Status**: PASS
- **Evidence**: Complete specification exists at `specs/1-k8s-todo-deployment/spec.md` with 21 functional requirements, 4 prioritized user stories, and 10 measurable success criteria
- **Compliance**: All implementation will map to explicit spec requirements (FR-001 through FR-021)

### ✅ Incremental Evolution
- **Status**: PASS
- **Evidence**: This is Phase IV (Local Kubernetes Deployment) following Phase II (web app with auth on HuggingFace)
- **Compliance**: Phase II remains functional and operational; Phase IV builds on top without breaking previous phases

### ✅ AI-Native Design
- **Status**: PASS
- **Evidence**: Using kubernetes-developer skill (FR-021) for all Kubernetes implementation; Claude Code as primary implementation assistant
- **Compliance**: Professional Kubernetes skill explicitly required for deployment design and implementation

### ✅ Code Quality and Documentation
- **Status**: PASS
- **Evidence**: Helm charts will be well-documented with values comments; Kubernetes resources follow best practices
- **Compliance**: Production-grade configuration with proper labels, annotations, and documentation

### ✅ Architecture-First Approach
- **Status**: PASS
- **Evidence**: Microservices architecture with separate frontend and backend services; clear service boundaries
- **Compliance**: Frontend and backend deployed as independent services with proper networking

### ✅ Container-First Deployment
- **Status**: PASS
- **Evidence**: Docker images pre-built; Kubernetes manifests via Helm charts; local testing on Minikube before cloud
- **Compliance**: This feature IS the container-first deployment implementation for Phase IV

**Overall Gate Status**: ✅ **PASS** - All constitution principles satisfied. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/1-k8s-todo-deployment/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology decisions and best practices
├── helm-chart-design.md # Phase 1: Helm chart structure and configuration design
├── quickstart.md        # Phase 1: Deployment quickstart guide
├── contracts/           # Phase 1: Configuration contracts
│   ├── backend-config.yaml    # Backend environment variables and settings
│   ├── frontend-config.yaml   # Frontend environment variables and settings
│   └── resource-limits.yaml   # Resource requests/limits specifications
└── tasks.md             # Phase 2: Granular implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
helm-charts/
└── todo-chatbot/              # Main Helm chart
    ├── Chart.yaml             # Chart metadata
    ├── values.yaml            # Default configuration values
    ├── values-dev.yaml        # Development environment overrides
    ├── templates/             # Kubernetes resource templates
    │   ├── _helpers.tpl       # Template helper functions
    │   ├── backend/
    │   │   ├── deployment.yaml    # Backend Deployment
    │   │   ├── service.yaml       # Backend Service (ClusterIP)
    │   │   └── configmap.yaml     # Backend ConfigMap (optional)
    │   ├── frontend/
    │   │   ├── deployment.yaml    # Frontend Deployment
    │   │   ├── service.yaml       # Frontend Service (NodePort/LoadBalancer)
    │   │   └── configmap.yaml     # Frontend ConfigMap (optional)
    │   └── NOTES.txt          # Post-install instructions
    └── .helmignore            # Files to exclude from chart

scripts/
├── load-images.sh         # Script to load Docker images into Minikube
├── deploy.sh              # Deployment automation script
├── validate.sh            # Post-deployment validation script
└── cleanup.sh             # Cleanup/teardown script

docs/
└── kubernetes/
    ├── deployment-guide.md    # Detailed deployment instructions
    ├── troubleshooting.md     # Common issues and solutions
    └── architecture.md        # Kubernetes architecture diagram
```

**Structure Decision**: Helm chart-based deployment structure chosen because:
1. Helm provides templating and configuration management required by FR-011 and FR-012
2. Separate backend/ and frontend/ template directories for clear service separation
3. Scripts directory for automation and validation tasks
4. Documentation directory for operational guides

## Complexity Tracking

> No constitution violations - this section not applicable.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

#### R1: Helm Chart Structure Best Practices
**Objective**: Determine optimal Helm chart organization for multi-service deployment

**Research Questions**:
- Should we use a single unified chart or separate charts for frontend/backend?
- What's the best practice for organizing templates with multiple services?
- How to structure values.yaml for clear service separation?

**Decision**: Use single unified Helm chart with separate template directories for each service
- **Rationale**: Simpler deployment (single `helm install` command), easier dependency management, shared configuration
- **Alternatives Considered**:
  - Separate charts: More complex, requires managing dependencies, harder to deploy atomically
  - Umbrella chart: Overkill for 2 services, adds unnecessary complexity

#### R2: Service Type Selection
**Objective**: Determine appropriate Kubernetes Service types for frontend and backend

**Research Questions**:
- Should frontend use NodePort or LoadBalancer in Minikube?
- Should backend use ClusterIP or expose externally?
- How to access services from host machine?

**Decision**:
- Frontend: NodePort (easier access in Minikube, no external load balancer needed)
- Backend: ClusterIP (internal only, accessed by frontend within cluster)

- **Rationale**: NodePort works well with Minikube's `minikube service` command; ClusterIP keeps backend internal for security
- **Alternatives Considered**:
  - LoadBalancer for frontend: Requires Minikube tunnel, more complex
  - NodePort for backend: Unnecessary external exposure, security risk

#### R3: Resource Limits Configuration
**Objective**: Determine appropriate CPU and memory limits for local Minikube deployment

**Research Questions**:
- What are reasonable resource requests/limits for local development?
- How to balance resource usage with Minikube constraints?
- What's the minimum viable configuration?

**Decision**:
- **Backend**: requests: 100m CPU, 128Mi memory; limits: 200m CPU, 256Mi memory
- **Frontend**: requests: 50m CPU, 64Mi memory; limits: 100m CPU, 128Mi memory

- **Rationale**: Conservative limits suitable for local development; allows 2-3 replicas within typical Minikube resources (4GB RAM)
- **Alternatives Considered**:
  - Higher limits: Would exhaust Minikube resources with multiple replicas
  - Lower limits: Risk of OOMKilled or CPU throttling

#### R4: Health Check Configuration
**Objective**: Design appropriate liveness and readiness probe configuration

**Research Questions**:
- What endpoints should probes check?
- What are appropriate timeouts and thresholds?
- How to handle startup delays?

**Decision**:
- **Liveness Probe**: HTTP GET to `/health` or `/healthz`, initialDelaySeconds: 30, periodSeconds: 10, timeoutSeconds: 5, failureThreshold: 3
- **Readiness Probe**: HTTP GET to `/ready` or `/health`, initialDelaySeconds: 5, periodSeconds: 5, timeoutSeconds: 3, failureThreshold: 3

- **Rationale**: Standard Kubernetes health check pattern; allows 30s for application startup; separate readiness for traffic control
- **Alternatives Considered**:
  - TCP probes: Less informative than HTTP, doesn't verify application health
  - Exec probes: More complex, requires shell in container

#### R5: Image Loading Strategy
**Objective**: Determine best method to load Docker images into Minikube

**Research Questions**:
- Should we use `minikube image load` or Minikube's Docker daemon?
- How to verify images are available?
- What's the most reliable approach?

**Decision**: Use Minikube's Docker daemon (`eval $(minikube docker-env)`) for image building/loading

- **Rationale**: More reliable, images persist in Minikube, no transfer overhead, works with existing Docker workflow
- **Alternatives Considered**:
  - `minikube image load`: Requires transferring images, slower, can fail with large images
  - Registry: Overkill for local development, adds complexity

#### R6: Replica Count Strategy
**Objective**: Determine appropriate replica counts for local deployment

**Research Questions**:
- How many replicas for high availability in local environment?
- What's the balance between HA and resource usage?
- Should replicas be configurable?

**Decision**:
- **Default**: 2 replicas per service (minimum for HA)
- **Configurable**: via Helm values for flexibility

- **Rationale**: 2 replicas provide basic HA without excessive resource usage; allows testing load distribution
- **Alternatives Considered**:
  - 1 replica: No HA, single point of failure
  - 3+ replicas: Excessive for local development, resource intensive

#### R7: Environment Variable Management
**Objective**: Determine how to manage environment variables for service configuration

**Research Questions**:
- Should we use ConfigMaps, Secrets, or direct env in Deployment?
- How to handle Phase II auth service URL?
- What's the most maintainable approach?

**Decision**:
- Use direct `env` in Deployment spec for non-sensitive config
- Use ConfigMap for shared configuration if needed
- No Secrets needed (no sensitive data in local deployment)

- **Rationale**: Simpler for local development; Phase II URL is public; direct env is more transparent in Helm templates
- **Alternatives Considered**:
  - ConfigMap for all config: Adds indirection, harder to template
  - Secrets: Unnecessary for public URLs and local development

### Research Summary

All research tasks completed. Key decisions documented above. Ready to proceed to Phase 1 design.

---

## Phase 1: Design & Contracts

### Helm Chart Design

#### Chart Metadata (Chart.yaml)
```yaml
apiVersion: v2
name: todo-chatbot
description: Helm chart for Todo AI Chatbot (Phase IV)
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - chatbot
  - ai
maintainers:
  - name: Fozia
```

#### Values Structure (values.yaml)

**Global Configuration**:
- `global.environment`: Environment name (dev, staging, prod)
- `global.imagePullPolicy`: IfNotPresent (for local images)

**Backend Configuration**:
- `backend.enabled`: true
- `backend.replicaCount`: 2
- `backend.image.repository`: phase4-backend
- `backend.image.tag`: latest
- `backend.service.type`: ClusterIP
- `backend.service.port`: 80
- `backend.service.targetPort`: 8000
- `backend.resources.requests`: {cpu: 100m, memory: 128Mi}
- `backend.resources.limits`: {cpu: 200m, memory: 256Mi}
- `backend.env.AUTH_SERVICE_URL`: https://fozi07-todo-full-stack-app.hf.space
- `backend.livenessProbe`: {path: /health, initialDelaySeconds: 30, periodSeconds: 10}
- `backend.readinessProbe`: {path: /health, initialDelaySeconds: 5, periodSeconds: 5}

**Frontend Configuration**:
- `frontend.enabled`: true
- `frontend.replicaCount`: 2
- `frontend.image.repository`: phase4-frontend
- `frontend.image.tag`: latest
- `frontend.service.type`: NodePort
- `frontend.service.port`: 80
- `frontend.service.targetPort`: 3000
- `frontend.service.nodePort`: 30080 (optional)
- `frontend.resources.requests`: {cpu: 50m, memory: 64Mi}
- `frontend.resources.limits`: {cpu: 100m, memory: 128Mi}
- `frontend.env.BACKEND_URL`: http://todo-chatbot-backend
- `frontend.livenessProbe`: {path: /health, initialDelaySeconds: 30, periodSeconds: 10}
- `frontend.readinessProbe`: {path: /health, initialDelaySeconds: 5, periodSeconds: 5}

#### Template Design

**Helper Templates (_helpers.tpl)**:
- `todo-chatbot.name`: Chart name
- `todo-chatbot.fullname`: Full resource name
- `todo-chatbot.chart`: Chart name and version
- `todo-chatbot.labels`: Common labels
- `todo-chatbot.selectorLabels`: Selector labels
- `todo-chatbot.backend.fullname`: Backend resource name
- `todo-chatbot.frontend.fullname`: Frontend resource name

**Backend Deployment Template**:
- Metadata: name, labels, annotations
- Spec: replicas, selector, strategy (RollingUpdate)
- Pod template: labels, containers, resources, probes, env
- Image pull policy: IfNotPresent
- Security context: non-root user

**Backend Service Template**:
- Type: ClusterIP
- Selector: backend labels
- Ports: 80 → 8000

**Frontend Deployment Template**:
- Similar structure to backend
- Different resource limits and env vars

**Frontend Service Template**:
- Type: NodePort
- Selector: frontend labels
- Ports: 80 → 3000, nodePort: 30080

### Configuration Contracts

#### Backend Configuration Contract

**File**: `specs/1-k8s-todo-deployment/contracts/backend-config.yaml`

```yaml
# Backend Service Configuration Contract
# This defines all configuration requirements for the backend service

service:
  name: backend
  type: ClusterIP
  port: 80
  targetPort: 8000

deployment:
  replicas: 2
  strategy: RollingUpdate
  maxSurge: 1
  maxUnavailable: 0

image:
  repository: phase4-backend
  tag: latest
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi

environment:
  required:
    - name: AUTH_SERVICE_URL
      value: https://fozi07-todo-full-stack-app.hf.space
      description: Phase II authentication service endpoint
  optional:
    - name: LOG_LEVEL
      value: info
      description: Application logging level
    - name: PORT
      value: "8000"
      description: Application listening port

healthChecks:
  liveness:
    path: /health
    port: 8000
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  readiness:
    path: /health
    port: 8000
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3

labels:
  app: todo-chatbot
  component: backend
  tier: api

annotations:
  description: "Backend API service for Todo AI Chatbot"
```

#### Frontend Configuration Contract

**File**: `specs/1-k8s-todo-deployment/contracts/frontend-config.yaml`

```yaml
# Frontend Service Configuration Contract
# This defines all configuration requirements for the frontend service

service:
  name: frontend
  type: NodePort
  port: 80
  targetPort: 3000
  nodePort: 30080

deployment:
  replicas: 2
  strategy: RollingUpdate
  maxSurge: 1
  maxUnavailable: 0

image:
  repository: phase4-frontend
  tag: latest
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 100m
    memory: 128Mi

environment:
  required:
    - name: BACKEND_URL
      value: http://todo-chatbot-backend
      description: Backend service URL (internal cluster DNS)
  optional:
    - name: PORT
      value: "3000"
      description: Application listening port

healthChecks:
  liveness:
    path: /health
    port: 3000
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3
  readiness:
    path: /health
    port: 3000
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3

labels:
  app: todo-chatbot
  component: frontend
  tier: web

annotations:
  description: "Frontend web application for Todo AI Chatbot"
```

#### Resource Limits Contract

**File**: `specs/1-k8s-todo-deployment/contracts/resource-limits.yaml`

```yaml
# Resource Limits Contract
# Defines resource allocation for all services

cluster:
  minimumRequirements:
    cpu: 2
    memory: 4Gi
    nodes: 1

services:
  backend:
    replicas: 2
    perPod:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi
    total:
      requests:
        cpu: 200m
        memory: 256Mi
      limits:
        cpu: 400m
        memory: 512Mi

  frontend:
    replicas: 2
    perPod:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 100m
        memory: 128Mi
    total:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 200m
        memory: 256Mi

totalClusterUsage:
  requests:
    cpu: 300m
    memory: 384Mi
  limits:
    cpu: 600m
    memory: 768Mi

headroom:
  available:
    cpu: 1700m  # 2000m - 300m
    memory: 3328Mi  # 4096Mi - 768Mi
  percentage:
    cpu: 85%
    memory: 81%
```

### Quickstart Guide

**File**: `specs/1-k8s-todo-deployment/quickstart.md`

```markdown
# Quickstart: Deploy Todo AI Chatbot to Minikube

## Prerequisites

- Minikube running with 4GB RAM, 2 CPUs minimum
- kubectl configured to communicate with Minikube
- Helm 3.x installed
- Docker images built: `phase4-frontend:latest`, `phase4-backend:latest`

## Quick Deployment (5 minutes)

### 1. Start Minikube
```bash
minikube start --cpus=4 --memory=8192
```

### 2. Load Docker Images
```bash
eval $(minikube docker-env)
docker images | grep phase4  # Verify images exist
```

### 3. Deploy with Helm
```bash
cd helm-charts/todo-chatbot
helm install todo-chatbot . --create-namespace --namespace todo-chatbot
```

### 4. Verify Deployment
```bash
kubectl get pods -n todo-chatbot
kubectl get services -n todo-chatbot
```

### 5. Access Frontend
```bash
minikube service todo-chatbot-frontend -n todo-chatbot
```

## Validation

### Check Pod Status
```bash
kubectl get pods -n todo-chatbot -w
# Wait for all pods to show STATUS: Running, READY: 1/1
```

### Test Backend Health
```bash
kubectl port-forward -n todo-chatbot svc/todo-chatbot-backend 8000:80
curl http://localhost:8000/health
```

### Test Frontend
```bash
# Open browser to URL from step 5
# Verify UI loads and can communicate with backend
```

### Test Authentication Flow
```bash
# In browser, attempt to authenticate
# Verify request flows: Frontend → Backend → Phase II Auth Service
```

## Troubleshooting

### Pods Not Starting
```bash
kubectl describe pod -n todo-chatbot <pod-name>
kubectl logs -n todo-chatbot <pod-name>
```

### Images Not Found
```bash
# Verify images in Minikube
eval $(minikube docker-env)
docker images | grep phase4

# If missing, rebuild or load images
```

### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints -n todo-chatbot

# Check Minikube service list
minikube service list
```

## Cleanup

```bash
helm uninstall todo-chatbot -n todo-chatbot
kubectl delete namespace todo-chatbot
```
```

---

## Phase 2: Implementation Tasks (Overview)

**Note**: Detailed granular tasks will be generated by `/sp.tasks` command. This section provides high-level task categories.

### Pre-Deployment Tasks
1. Verify Minikube cluster status and resources
2. Verify Docker images exist locally
3. Verify kubectl and Helm installation
4. Verify Phase II authentication service accessibility
5. Create Helm chart directory structure

### Helm Chart Creation Tasks
6. Create Chart.yaml with metadata
7. Create values.yaml with default configuration
8. Create _helpers.tpl with template functions
9. Create backend Deployment template
10. Create backend Service template
11. Create frontend Deployment template
12. Create frontend Service template
13. Create NOTES.txt with post-install instructions
14. Create .helmignore file

### Deployment Tasks
15. Load Docker images into Minikube
16. Validate Helm chart syntax (helm lint)
17. Perform dry-run deployment (helm install --dry-run)
18. Deploy Helm chart to Minikube
19. Monitor pod startup and readiness

### Validation Tasks
20. Verify all pods are running and ready
21. Verify services have endpoints
22. Test backend health endpoint
23. Test frontend accessibility from host
24. Test frontend-to-backend communication
25. Test end-to-end authentication flow
26. Verify resource usage within limits
27. Test pod failure recovery (delete pod, verify recreation)

### Documentation Tasks
28. Create deployment guide
29. Create troubleshooting guide
30. Document configuration options
31. Create architecture diagram

### Post-Deployment Tasks
32. Test Helm upgrade with configuration change
33. Test Helm rollback
34. Document cleanup procedures
35. Create validation checklist

---

## Implementation Sequence

### Phase 0: Research (Completed Above)
- All technology decisions documented
- Best practices identified
- Configuration contracts defined

### Phase 1: Design (Completed Above)
- Helm chart structure designed
- Configuration contracts created
- Quickstart guide written

### Phase 2: Implementation (To be executed via /sp.tasks)
1. **Pre-Deployment Validation** (Tasks 1-5)
2. **Helm Chart Creation** (Tasks 6-14)
3. **Deployment Execution** (Tasks 15-19)
4. **Post-Deployment Validation** (Tasks 20-27)
5. **Documentation** (Tasks 28-31)
6. **Operational Testing** (Tasks 32-35)

---

## Success Criteria Mapping

| Success Criterion | Validation Method | Task Reference |
|-------------------|-------------------|----------------|
| SC-001: Deploy within 2 minutes | Time deployment from helm install to all pods ready | Task 18-19 |
| SC-002: Pods ready within 60s | Monitor pod status with kubectl get pods -w | Task 20 |
| SC-003: Frontend accessible within 10s | Access frontend URL after deployment | Task 23 |
| SC-004: Auth response < 3s | Test authentication flow, measure response time | Task 26 |
| SC-005: 99% uptime, 30s recovery | Delete pod, verify automatic recreation | Task 27 |
| SC-006: 10+ concurrent sessions | Load test with multiple browser sessions | Task 26 |
| SC-007: Helm upgrade < 1 minute | Time helm upgrade operation | Task 32 |
| SC-008: Resources within limits | Check kubectl top pods | Task 26 |
| SC-009: Probes detect failure < 10s | Simulate unhealthy pod, monitor restart | Task 27 |
| SC-010: Redeploy within 3 minutes | Time full cleanup and redeploy cycle | Task 35 |

---

## Risk Mitigation

### High Priority Risks

**R1: External Service Dependency (Phase II Auth)**
- **Mitigation**: Validate connectivity before deployment (Task 4)
- **Fallback**: Document error handling in troubleshooting guide
- **Monitoring**: Include auth service health check in validation

**R2: Resource Constraints (Minikube)**
- **Mitigation**: Conservative resource limits (100m CPU, 128Mi memory)
- **Validation**: Verify cluster resources before deployment (Task 1)
- **Monitoring**: Track resource usage during validation (Task 26)

**R3: Network Connectivity**
- **Mitigation**: Test Phase II service accessibility pre-deployment (Task 4)
- **Validation**: End-to-end auth flow test (Task 26)
- **Documentation**: Network requirements in troubleshooting guide

### Medium Priority Risks

**R4: Image Loading Failures**
- **Mitigation**: Use Minikube Docker daemon for reliability
- **Validation**: Verify images before deployment (Task 2, 15)
- **Fallback**: Document image loading troubleshooting

**R5: Configuration Errors**
- **Mitigation**: Helm lint and dry-run before deployment (Task 16-17)
- **Validation**: Review generated manifests in dry-run output
- **Testing**: Test with different values configurations

**R6: Health Check Failures**
- **Mitigation**: Conservative probe settings (30s initial delay)
- **Validation**: Test health endpoints before deployment
- **Monitoring**: Watch pod events for probe failures

---

## Dependencies & Prerequisites

### Must Be Satisfied Before Implementation

1. ✅ **Specification Complete**: spec.md exists and validated
2. ✅ **Constitution Check Passed**: All gates satisfied
3. ✅ **Research Complete**: All technology decisions made
4. ⏳ **Minikube Running**: Cluster operational with sufficient resources
5. ⏳ **Docker Images Built**: phase4-frontend:latest and phase4-backend:latest exist
6. ⏳ **Tools Installed**: kubectl, Helm, Docker CLI available
7. ⏳ **Phase II Service Operational**: https://fozi07-todo-full-stack-app.hf.space accessible
8. ⏳ **Network Connectivity**: Internet access for external service communication

### Will Be Created During Implementation

- Helm chart directory structure
- Kubernetes resource templates
- Configuration files
- Deployment scripts
- Validation scripts
- Documentation

---

## Next Steps

1. **Review this plan** for completeness and accuracy
2. **Run `/sp.tasks`** to generate granular implementation tasks from this plan
3. **Execute tasks sequentially** following the implementation sequence
4. **Use kubernetes-developer skill** for all Kubernetes resource creation and configuration
5. **Validate each phase** before proceeding to next
6. **Document issues** encountered during implementation
7. **Update plan** if significant deviations occur

---

## Notes

### Implementation Approach

- **kubernetes-developer skill**: Must be used for all Kubernetes resource design, Helm template creation, and cluster configuration (per FR-021)
- **Incremental validation**: Validate each component before proceeding (backend first, then frontend)
- **Configuration management**: All settings via Helm values for flexibility
- **Production-grade**: Even for local deployment, follow production best practices
- **Documentation-first**: Document as you implement for reproducibility

### Key Decisions

1. **Single Helm chart**: Simpler deployment, easier management
2. **NodePort for frontend**: Best for Minikube access
3. **ClusterIP for backend**: Internal only, security best practice
4. **Conservative resources**: Fits within Minikube constraints
5. **2 replicas default**: Minimum for HA testing
6. **Direct env vars**: Simpler than ConfigMaps for local deployment

### Testing Strategy

- **Unit**: Helm lint, dry-run validation
- **Integration**: Pod startup, service connectivity
- **End-to-end**: Full authentication flow through all services
- **Resilience**: Pod failure and recovery
- **Performance**: Resource usage, response times

---

**Plan Status**: ✅ Complete - Ready for task generation via `/sp.tasks`
