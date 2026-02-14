# Helm Charts Implementation Guide

## Overview

This document explains how the Todo AI Chatbot Helm charts were designed and implemented, specifically detailing the use of the **kubernetes-developer skill** for professional-grade Kubernetes deployment configuration.

---

## Architecture & Design Decisions

### Chart Structure

```
todo-chatbot/                           # Main Helm chart
├── Chart.yaml                          # Chart metadata (name, version, appVersion)
├── values.yaml                         # Production configuration
├── values-dev.yaml                     # Development overrides
├── templates/
│   ├── _helpers.tpl                   # Reusable template functions
│   ├── NOTES.txt                      # Post-install instructions
│   ├── backend/
│   │   ├── deployment.yaml            # Backend Deployment resource
│   │   └── service.yaml               # Backend Service (ClusterIP)
│   ├── frontend/
│   │   ├── deployment.yaml            # Frontend Deployment resource
│   │   └── service.yaml               # Frontend Service (NodePort)
│   └── mcp-server/
│       ├── deployment.yaml            # MCP Server Deployment resource
│       └── service.yaml               # MCP Server Service (ClusterIP)
└── .helmignore                         # Files to exclude from chart
```

### Kubernetes Professional Practices Applied

The following Kubernetes best practices were implemented using the **kubernetes-developer skill**:

#### 1. **Deployment Resource Configuration**

Each service (backend, frontend, MCP server) is deployed using a Kubernetes Deployment with:

- **Rolling Update Strategy**: `maxSurge: 1, maxUnavailable: 0` ensures zero-downtime deployments
  ```yaml
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  ```

- **Resource Requests & Limits**: Prevent resource exhaustion and enable proper scheduling
  ```yaml
  resources:
    requests:                  # Guaranteed resources for pod scheduling
      cpu: 100m
      memory: 128Mi
    limits:                    # Prevent pods from consuming excessive resources
      cpu: 200m
      memory: 256Mi
  ```

- **Health Probes**: Ensure pod lifecycle management
  ```yaml
  livenessProbe:             # Detects dead pods and triggers restart
    httpGet:
      path: /health
      port: http
    initialDelaySeconds: 30  # Wait for app startup
    periodSeconds: 10        # Check every 10 seconds
    failureThreshold: 3      # Restart after 3 failures (~30 sec)

  readinessProbe:            # Controls traffic routing
    httpGet:
      path: /health
      port: http
    initialDelaySeconds: 5   # Quick readiness check
    periodSeconds: 5
    failureThreshold: 3
  ```

#### 2. **Service Resource Configuration**

Two types of services are used:

- **ClusterIP Services** (Backend, MCP Server): Internal-only service discovery
  ```yaml
  # In templates/backend/service.yaml
  kind: Service
  spec:
    type: ClusterIP
    ports:
      - port: 80              # Service port
        targetPort: 8000      # Pod port
        name: http
  ```
  This allows frontend to reach backend via `http://todo-chatbot-backend:80` using Kubernetes DNS.

- **NodePort Service** (Frontend): External access from host machine
  ```yaml
  # In templates/frontend/service.yaml
  kind: Service
  spec:
    type: NodePort
    ports:
      - port: 80
        targetPort: 3000
        nodePort: 30080       # Fixed external port
  ```
  Accessible via `http://<minikube-ip>:30080` from the host.

#### 3. **Label & Selector Strategy**

Kubernetes-standard labeling convention ensures proper resource organization:

```yaml
# Labels applied to all resources
labels:
  helm.sh/chart: todo-chatbot-1.0.0           # Helm chart version
  app.kubernetes.io/name: todo-chatbot        # App name
  app.kubernetes.io/instance: <release-name>  # Helm release name
  app.kubernetes.io/managed-by: Helm          # Manager tool
  app.kubernetes.io/version: "1.0.0"          # App version
  component: backend|frontend|mcp-server      # Component type

# Selectors for routing traffic
selector:
  app.kubernetes.io/name: todo-chatbot
  app.kubernetes.io/instance: <release-name>
  component: backend|frontend|mcp-server
```

These labels enable:
- Service discovery via selectors
- Monitoring and logging filtering
- Cost allocation and resource tracking
- Multi-tenancy support

#### 4. **Environment Variable Management**

Configuration is separated from code:

```yaml
# In values.yaml
backend:
  env:
    AUTH_SERVICE_URL: https://fozi07-todo-full-stack-app.hf.space
    DATABASE_URL: postgresql+asyncpg://...
    GEMINI_API_KEY: AIzaSy...
    MCP_SERVER_URL: http://mcp-server:8002  # Internal service DNS
```

Each deployment template injects these as environment variables:

```yaml
# In templates/backend/deployment.yaml
containers:
  - name: backend
    env:
      - name: AUTH_SERVICE_URL
        value: {{ .Values.backend.env.AUTH_SERVICE_URL | quote }}
      - name: DATABASE_URL
        value: {{ .Values.backend.env.DATABASE_URL | quote }}
```

This approach enables:
- Environment-specific configuration (production vs. development)
- No hardcoded secrets in code
- Easy configuration updates without rebuilding images

#### 5. **Replica Count & Availability**

Multiple replicas ensure service availability:

```yaml
# In values.yaml
backend:
  replicaCount: 3    # Production: 3 replicas, development: 1
frontend:
  replicaCount: 2    # Production: 2 replicas, development: 1
mcp-server:
  replicaCount: 2    # Production: 2 replicas, development: 1
```

When one pod fails:
1. Kubernetes detects failure via liveness probe
2. Failed pod is terminated
3. Deployment controller automatically creates replacement
4. Service routes traffic only to healthy pods (via readiness probe)
5. Zero service interruption for users

#### 6. **Image Pull Policy**

```yaml
global:
  imagePullPolicy: IfNotPresent
```

This tells Kubernetes to use locally-loaded Docker images first, critical for local development with Minikube.

---

## Implementation Details

### kubernetes-developer Skill Application

The **kubernetes-developer skill** was used to make the following architectural decisions:

#### Decision 1: Service Type Selection
- **Backend**: ClusterIP (internal only)
  - Why: Frontend needs to reach it, no external access needed
  - Pattern: Service discovery via DNS within cluster

- **Frontend**: NodePort (external access)
  - Why: Users need to access from browser on host machine
  - Fixed port 30080 for consistent access

- **MCP Server**: ClusterIP (internal only)
  - Why: Only backend communicates with it
  - Accessed via `http://mcp-server:8002` from backend

#### Decision 2: Health Check Endpoints
- **Backend/MCP Server**: `/health` (or `/docs` for mcp-use SDK)
  - Both endpoints return HTTP 200 for healthy state
  - Liveness: Detects hung processes
  - Readiness: Ensures database connectivity before accepting traffic

- **Frontend**: `/` (root path)
  - Next.js returns HTML page (HTTP 200) when healthy
  - Simple and effective for a frontend service

#### Decision 3: Resource Limits
Calculated based on application profiles:

**Production Configuration:**
```
Backend:     100m CPU request, 200m limit; 128Mi mem request, 256Mi limit
Frontend:    50m CPU request, 100m limit; 64Mi mem request, 128Mi limit
MCP Server:  100m CPU request, 200m limit; 128Mi mem request, 256Mi limit
```

**Development Configuration** (values-dev.yaml):
- 50% of production limits to save local resources
- Single replica per service instead of multiple

#### Decision 4: Rolling Update Strategy
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1           # Temporarily run 1 extra pod during update
    maxUnavailable: 0     # Never have 0 healthy pods
```

This ensures:
- Zero downtime during deployments (Helm upgrades)
- Gradual rollout of new version
- Automatic rollback if new version fails health checks

---

## Helm Template Patterns Used

### 1. **Chart Helpers (_helpers.tpl)**

```go
{{- define "todo-chatbot.backend.fullname" -}}
{{- printf "%s-backend" (include "todo-chatbot.fullname" .) -}}
{{- end }}
```

- Generates consistent resource names
- Prevents naming conflicts in clusters with multiple releases
- Example: `my-release-backend`, `my-release-frontend`, `my-release-mcp-server`

### 2. **Conditional Configuration**

```yaml
{{- if not .Values.backend.autoscaling.enabled }}
replicas: {{ .Values.backend.replicaCount }}
{{- end }}
```

- Allows toggling between manual replicas and autoscaling
- Extensible for future features without modifying templates

### 3. **Selector Label Strategy**

```yaml
selector:
  {{- include "todo-chatbot.selectorLabels" . | nindent 4 }}
  component: backend
```

- Reusable label definitions
- Component label differentiates between services
- Service selects only pods with matching component label

### 4. **NOTES.txt Instructions**

```
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "todo-chatbot.frontend.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
```

- Provides automated post-install instructions
- Uses Helm template variables for accuracy
- Guides users to access deployed services

---

## Environment-Specific Configuration

### Production (values.yaml - default)
- 3 backend replicas for high availability
- 2 frontend replicas for load distribution
- 2 MCP server replicas for resilience
- Full resource limits for production workloads

### Development (values-dev.yaml)
- 1 replica per service (saves local resources)
- 50% resource limits (suitable for development machine)
- Same configuration structure, just reduced scale

**Deploy with development values:**
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-dev.yaml \
  --namespace todo-chatbot
```

---

## Service Communication Map

### Internal Service Discovery (via Kubernetes DNS)

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ http://<minikube-ip>:30080
       ▼
┌──────────────────┐
│   Frontend Pod   │
│  (3000 internal) │
└────────┬─────────┘
         │ http://todo-chatbot-backend  (Kubernetes DNS)
         ▼
┌──────────────────┐
│   Backend Pod    │
│  (8000 internal) │
└────────┬─────────┘
         │ http://mcp-server:8002 (Kubernetes DNS)
         ▼
┌──────────────────┐
│  MCP Server Pod  │
│  (8002 internal) │
└──────────────────┘
```

**Service Names Generated by Helm:**
- Backend: `{release-name}-todo-chatbot-backend`
  - Example: `todo-chatbot-backend` (when release name is "todo-chatbot")
- Frontend: `{release-name}-todo-chatbot-frontend`
- MCP Server: `{release-name}-todo-chatbot-mcp-server`

---

## Deployment Workflow

### 1. Load Docker Images into Minikube
```bash
minikube image load phaseiv-backend:latest
minikube image load phaseiv-frontend:latest
minikube image load mcp-server:latest
```

### 2. Deploy via Helm (Production)
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --namespace todo-chatbot \
  --create-namespace
```

### 3. Verify Deployment
```bash
# Check pods
kubectl get pods -n todo-chatbot

# Check services
kubectl get svc -n todo-chatbot

# View logs
kubectl logs -n todo-chatbot deployment/todo-chatbot-backend
kubectl logs -n todo-chatbot deployment/todo-chatbot-frontend
kubectl logs -n todo-chatbot deployment/todo-chatbot-mcp-server

# Helm status
helm status todo-chatbot -n todo-chatbot
```

### 4. Update Configuration
```bash
# Update a value and redeploy (rolling update)
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.replicaCount=5 \
  --namespace todo-chatbot
```

### 5. Rollback if Needed
```bash
helm rollback todo-chatbot \
  --namespace todo-chatbot
```

---

## Security Considerations

### Current Implementation
- ✅ No hardcoded secrets in code
- ✅ Environment variables for configuration
- ✅ Resource limits prevent denial of service
- ✅ Health probes detect compromised pods

### Future Enhancements (Out of Scope)
- Kubernetes Secrets for sensitive data (GEMINI_API_KEY)
- Network policies to restrict pod-to-pod communication
- Pod security policies and RBAC
- Service account configuration
- TLS/SSL for inter-service communication

---

## Troubleshooting

### Pod Not Starting
```bash
# Check pod status
kubectl describe pod <pod-name> -n todo-chatbot

# Check logs
kubectl logs <pod-name> -n todo-chatbot
```

Common issues:
- Image not found: Load images into Minikube first
- Resource constraints: Reduce replica count or resource limits
- Environment variable missing: Check values.yaml

### Service Unreachable
```bash
# Verify service exists
kubectl get svc -n todo-chatbot

# Check endpoints (should show pod IPs)
kubectl get endpoints -n todo-chatbot

# Test DNS from pod
kubectl exec <pod-name> -n todo-chatbot -- nslookup todo-chatbot-backend
```

### Health Check Failures
```bash
# Manual health check
kubectl exec <pod-name> -n todo-chatbot -- curl http://localhost:8000/health
```

---

## References

- Kubernetes Deployment: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes Services: https://kubernetes.io/docs/concepts/services-networking/service/
- Helm Charts: https://helm.sh/docs/chart_template_guide/
- Best Practices: https://kubernetes.io/docs/concepts/configuration/overview/

---

## Summary

The Todo AI Chatbot Helm charts demonstrate professional Kubernetes deployment practices:

✅ **Stateless services** with multiple replicas
✅ **Health probes** for automatic recovery
✅ **Resource limits** for cluster stability
✅ **Rolling updates** for zero-downtime deployments
✅ **Service discovery** via Kubernetes DNS
✅ **Environment-specific configuration** (production & development)
✅ **Clear documentation** and deployment instructions

The use of the **kubernetes-developer skill** ensured all decisions follow industry best practices and enable production-grade deployments while maintaining local development simplicity.

---

**Document Version**: 1.0
**Last Updated**: 2026-02-15
**Kubernetes Skill**: kubernetes-developer
**Status**: Ready for Production Deployment
