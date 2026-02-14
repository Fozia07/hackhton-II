# Research: Kubernetes Deployment Technology Decisions

**Feature**: Local Kubernetes Deployment of Todo AI Chatbot
**Date**: 2026-02-09
**Status**: Complete

## Overview

This document captures all technology decisions, best practices research, and architectural choices for deploying the Todo AI Chatbot to local Kubernetes using Helm and Minikube.

---

## R1: Helm Chart Structure Best Practices

### Research Question
Should we use a single unified chart or separate charts for frontend/backend services?

### Options Evaluated

**Option A: Single Unified Chart**
- All services in one chart with separate template directories
- Single `helm install` command
- Shared configuration and dependencies
- Simpler version management

**Option B: Separate Charts per Service**
- Independent charts for frontend and backend
- Requires managing chart dependencies
- More complex deployment (multiple helm commands or umbrella chart)
- Better service isolation

**Option C: Umbrella Chart with Subcharts**
- Parent chart with frontend/backend as dependencies
- Most complex structure
- Overkill for 2 services

### Decision: **Option A - Single Unified Chart**

**Rationale**:
- Simpler deployment experience (single command)
- Easier dependency management between services
- Shared configuration (labels, annotations, common values)
- Atomic deployment (both services deployed together)
- Easier rollback (single release)
- Appropriate complexity for 2 services

**Implementation Details**:
```
todo-chatbot/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── backend/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── frontend/
        ├── deployment.yaml
        └── service.yaml
```

**References**:
- Helm Best Practices: https://helm.sh/docs/chart_best_practices/
- Multi-service chart patterns from kubernetes-developer skill

---

## R2: Service Type Selection

### Research Question
What Kubernetes Service types should be used for frontend and backend in Minikube?

### Options Evaluated

**Frontend Service Options**:
1. **NodePort**: Exposes service on each node's IP at a static port (30000-32767)
2. **LoadBalancer**: Requests external load balancer (requires Minikube tunnel)
3. **ClusterIP**: Internal only (not suitable for user access)

**Backend Service Options**:
1. **ClusterIP**: Internal cluster access only
2. **NodePort**: External access (unnecessary for internal API)
3. **LoadBalancer**: External load balancer (overkill for internal service)

### Decision: Frontend = NodePort, Backend = ClusterIP

**Rationale**:

**Frontend (NodePort)**:
- Works seamlessly with Minikube's `minikube service` command
- No need for external load balancer in local environment
- Simple access from host machine browser
- Port range 30000-32767 avoids conflicts with common services
- Can specify nodePort: 30080 for consistent access

**Backend (ClusterIP)**:
- Internal-only access maintains security best practice
- Frontend accesses via cluster DNS (http://todo-chatbot-backend)
- No unnecessary external exposure
- Standard pattern for internal microservices

**Implementation**:
```yaml
# Frontend Service
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 3000
    nodePort: 30080

# Backend Service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8000
```

**Access Methods**:
- Frontend: `minikube service todo-chatbot-frontend` or `http://<minikube-ip>:30080`
- Backend: Internal DNS `http://todo-chatbot-backend` (from frontend pods)

**References**:
- Kubernetes Service Types: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
- Minikube service access: https://minikube.sigs.k8s.io/docs/handbook/accessing/

---

## R3: Resource Limits Configuration

### Research Question
What are appropriate CPU and memory limits for local Minikube deployment?

### Constraints
- Minikube minimum: 4GB RAM, 2 CPUs
- Need to run 2 services with 2 replicas each (4 pods total)
- Leave headroom for Kubernetes system components
- Support local development workload

### Calculation

**Kubernetes System Overhead**: ~500-700Mi memory, ~200-300m CPU

**Available for Applications**: ~3.3Gi memory, ~1.7 CPUs

**Per-Service Allocation**:

**Backend** (more resource-intensive, handles auth logic):
- Requests: 100m CPU, 128Mi memory
- Limits: 200m CPU, 256Mi memory
- 2 replicas = 200m CPU, 256Mi memory (requests)

**Frontend** (lighter, serves static content):
- Requests: 50m CPU, 64Mi memory
- Limits: 100m CPU, 128Mi memory
- 2 replicas = 100m CPU, 128Mi memory (requests)

**Total Usage**:
- Requests: 300m CPU, 384Mi memory
- Limits: 600m CPU, 768Mi memory
- Headroom: 1400m CPU (70%), 2944Mi memory (88%)

### Decision: Conservative Limits with Headroom

**Rationale**:
- Leaves 70%+ headroom for system components and spikes
- Prevents resource exhaustion in local environment
- Allows comfortable operation within Minikube constraints
- Supports 2 replicas per service for HA testing
- Realistic for development workload

**Risk Mitigation**:
- If pods are OOMKilled, increase memory limits
- If CPU throttling occurs, increase CPU limits
- Monitor with `kubectl top pods` during validation

**References**:
- Kubernetes Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Resource QoS Classes: https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/

---

## R4: Health Check Configuration

### Research Question
How should liveness and readiness probes be configured for reliable health checking?

### Probe Types Evaluated

1. **HTTP GET**: Checks HTTP endpoint, most informative
2. **TCP Socket**: Checks port connectivity, less informative
3. **Exec**: Runs command in container, most flexible but complex

### Decision: HTTP GET Probes

**Liveness Probe Configuration**:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

**Readiness Probe Configuration**:
```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Rationale**:

**Liveness Probe**:
- 30s initial delay: Allows application startup time
- 10s period: Checks every 10 seconds
- 5s timeout: Reasonable for local network
- 3 failures: 30 seconds before restart (3 × 10s)
- Prevents premature restarts during startup

**Readiness Probe**:
- 5s initial delay: Quick readiness check
- 5s period: Frequent checks for traffic control
- 3s timeout: Fast response expected
- 3 failures: 15 seconds before removing from service
- Ensures only healthy pods receive traffic

**Endpoint Requirements**:
- Both services must expose `/health` endpoint
- Should return 200 OK when healthy
- Should check critical dependencies (e.g., backend checks Phase II auth connectivity)

**References**:
- Kubernetes Probes: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Health Check Best Practices from kubernetes-developer skill

---

## R5: Image Loading Strategy

### Research Question
What's the best method to load Docker images into Minikube?

### Options Evaluated

**Option A: minikube image load**
```bash
minikube image load phase4-backend:latest
minikube image load phase4-frontend:latest
```
- Transfers images from host to Minikube
- Can be slow for large images
- May fail with large images or limited resources

**Option B: Minikube Docker Daemon**
```bash
eval $(minikube docker-env)
docker build -t phase4-backend:latest .
# Images built directly in Minikube
```
- Uses Minikube's Docker daemon directly
- No image transfer needed
- Images persist in Minikube
- More reliable

**Option C: Local Registry**
- Set up local Docker registry
- Push images to registry
- Pull from registry in Minikube
- Overkill for local development

### Decision: **Option B - Minikube Docker Daemon**

**Rationale**:
- Most reliable for local development
- No image transfer overhead
- Images persist in Minikube VM
- Works with existing Docker workflow
- Simpler than registry setup
- Recommended by Minikube documentation

**Implementation**:
```bash
# Point Docker CLI to Minikube's daemon
eval $(minikube docker-env)

# Verify images exist (or build them)
docker images | grep phase4

# Deploy with imagePullPolicy: IfNotPresent
```

**Important**: Set `imagePullPolicy: IfNotPresent` or `Never` in Helm values to use local images.

**References**:
- Minikube Docker Daemon: https://minikube.sigs.k8s.io/docs/handbook/pushing/#1-pushing-directly-to-the-in-cluster-docker-daemon-docker-env
- Image Pull Policy: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy

---

## R6: Replica Count Strategy

### Research Question
How many replicas should be deployed for each service in local environment?

### Options Evaluated

**1 Replica**:
- Minimal resource usage
- No high availability
- Single point of failure
- Cannot test load distribution

**2 Replicas**:
- Minimum for high availability
- Can test load distribution
- Reasonable resource usage
- Survives single pod failure

**3+ Replicas**:
- Better HA and load distribution
- Higher resource usage
- May exceed Minikube resources
- Overkill for local development

### Decision: **2 Replicas (Default, Configurable)**

**Rationale**:
- Minimum viable HA configuration
- Allows testing pod failure recovery
- Enables load distribution testing
- Fits within Minikube resource constraints
- Configurable via Helm values for flexibility

**Implementation**:
```yaml
# values.yaml
backend:
  replicaCount: 2

frontend:
  replicaCount: 2
```

**Scaling Options**:
```bash
# Scale up for testing
helm upgrade todo-chatbot . --set backend.replicaCount=3

# Scale down for resource constraints
helm upgrade todo-chatbot . --set backend.replicaCount=1
```

**References**:
- Kubernetes Deployments: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- High Availability Patterns from kubernetes-developer skill

---

## R7: Environment Variable Management

### Research Question
How should environment variables be managed for service configuration?

### Options Evaluated

**Option A: Direct env in Deployment**
```yaml
env:
- name: AUTH_SERVICE_URL
  value: https://fozi07-todo-full-stack-app.hf.space
```
- Simple and transparent
- Easy to template in Helm
- No indirection

**Option B: ConfigMap**
```yaml
envFrom:
- configMapRef:
    name: backend-config
```
- Separates config from deployment
- Reusable across resources
- Adds indirection

**Option C: Secrets**
```yaml
envFrom:
- secretRef:
    name: backend-secrets
```
- For sensitive data
- Base64 encoded
- Not needed for public URLs

### Decision: **Option A - Direct env in Deployment**

**Rationale**:
- Simpler for local development
- Phase II auth URL is public (no secret needed)
- More transparent in Helm templates
- Easier to override via Helm values
- No sensitive data in local deployment

**When to Use ConfigMap**:
- Multiple pods need same config
- Config is large or complex
- Want to update config without redeploying

**When to Use Secrets**:
- Sensitive data (passwords, API keys, tokens)
- Production deployments
- Not applicable for this local deployment

**Implementation**:
```yaml
# Backend Deployment
env:
- name: AUTH_SERVICE_URL
  value: {{ .Values.backend.env.AUTH_SERVICE_URL }}
- name: LOG_LEVEL
  value: {{ .Values.backend.env.LOG_LEVEL | default "info" }}

# Frontend Deployment
env:
- name: BACKEND_URL
  value: http://{{ include "todo-chatbot.backend.fullname" . }}
- name: PORT
  value: "3000"
```

**References**:
- Kubernetes Environment Variables: https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/
- ConfigMaps vs Secrets: https://kubernetes.io/docs/concepts/configuration/configmap/

---

## Summary of Decisions

| Decision Area | Choice | Rationale |
|---------------|--------|-----------|
| Chart Structure | Single unified chart | Simpler deployment, shared config |
| Frontend Service | NodePort | Easy Minikube access |
| Backend Service | ClusterIP | Internal only, security |
| Backend Resources | 100m/200m CPU, 128Mi/256Mi memory | Balanced for local dev |
| Frontend Resources | 50m/100m CPU, 64Mi/128Mi memory | Lighter workload |
| Health Probes | HTTP GET to /health | Most informative |
| Image Loading | Minikube Docker daemon | Most reliable |
| Replica Count | 2 per service | Minimum HA |
| Environment Vars | Direct in Deployment | Simpler for local dev |

---

## Implementation Readiness

All research complete. Key decisions documented with rationale. Ready to proceed to Phase 1 design and contract creation.

**Next Steps**:
1. Create Helm chart structure based on decisions
2. Implement configuration contracts
3. Generate Kubernetes resource templates
4. Create deployment and validation scripts
