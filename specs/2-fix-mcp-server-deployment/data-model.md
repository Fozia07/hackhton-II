# Data Model: Kubernetes Resources

**Feature**: Fix MCP Server Deployment Issues
**Date**: 2026-02-13
**Type**: Infrastructure / Kubernetes Resources

## Overview

This document defines the Kubernetes resource structure for the MCP server deployment. Unlike traditional data models, this focuses on declarative infrastructure resources.

## Resource Entities

### 1. Deployment (apps/v1)

**Purpose**: Manages MCP server pod replicas and lifecycle

**Entity**: `mcp-server` Deployment

**Key Attributes**:
- **namespace**: `todo-chatbot` - Isolates chatbot services
- **replicas**: `2` - High availability with load distribution
- **selector**: `app: mcp-server` - Pod selection criteria
- **strategy**: Rolling update (implicit default)

**Pod Template Specification**:

| Field | Value | Validation Rule | Purpose |
|-------|-------|----------------|---------|
| `image` | `mcp-server:latest` | Must exist in Minikube | Local build reference |
| `imagePullPolicy` | `IfNotPresent` | Must be IfNotPresent/Never for local | Prevents external registry pulls |
| `containerPort` | `8002` | Must match service targetPort | MCP server HTTP port |
| `resources.requests.cpu` | `100m` | 0.1 CPU minimum | Scheduling guarantee |
| `resources.requests.memory` | `128Mi` | 128 MiB minimum | Scheduling guarantee |
| `resources.limits.cpu` | `200m` | 0.2 CPU maximum | Prevents resource hogging |
| `resources.limits.memory` | `256Mi` | 256 MiB maximum | Prevents OOM kills on node |

**Environment Variables**:

| Variable | Value | Purpose |
|----------|-------|---------|
| `PORT` | `8002` | Server listen port |
| `MCP_SERVER_PORT` | `8002` | MCP protocol port |
| `LOG_LEVEL` | `info` | Logging verbosity |

**State Transitions**:

```
Deployment Created
    ↓
ReplicaSet Created (2 replicas)
    ↓
Pods Scheduled → Pending
    ↓
Image Pull (IfNotPresent) → ImagePullBackOff if not loaded
    ↓ (after fix)
Container Starting → Running
    ↓
Readiness Probe → Ready (after 5s)
    ↓
Liveness Probe → Healthy (continuous)
```

### 2. Service (v1)

**Purpose**: Provides stable DNS name and load balancing for MCP server pods

**Entity**: `mcp-server` Service

**Key Attributes**:
- **namespace**: `todo-chatbot` - Must match deployment namespace
- **type**: `ClusterIP` - Internal cluster access only
- **selector**: `app: mcp-server` - Routes to deployment pods
- **port**: `8002` - Service port (external to service)
- **targetPort**: `8002` - Container port (internal to pod)

**DNS Resolution**:
- Within namespace: `mcp-server:8002`
- Cross-namespace: `mcp-server.todo-chatbot.svc.cluster.local:8002`
- Backend service uses: `http://mcp-server:8002`

**Load Balancing**:
- Algorithm: Round-robin across ready pods
- Session affinity: None (stateless service)
- Health checks: Only routes to pods passing readiness probe

### 3. Pod (v1) - Runtime Instance

**Purpose**: Runs single MCP server container instance

**Entity**: Pod created by Deployment

**Container Specification**:

| Aspect | Configuration | Validation |
|--------|--------------|------------|
| **Image** | `mcp-server:latest` | Must exist via `minikube image load` |
| **Working Directory** | `/app` (implicit from Dockerfile) | Must contain `mcp_server_entry.py` |
| **Command** | `["python", "mcp_server_entry.py"]` | Must execute without ImportError |
| **Port** | `8002/TCP` | Must be available (not conflicting) |

**Probe Configuration**:

| Probe Type | Path | Initial Delay | Period | Timeout | Failure Threshold |
|------------|------|---------------|--------|---------|-------------------|
| **Liveness** | `/health` | 30s | 10s | 5s | 3 |
| **Readiness** | `/ready` | 5s | 5s | 3s | 3 |

**Liveness Probe** (Pod restart trigger):
- Checks if server process is alive
- Initial delay: 30s (allows server startup)
- Failure threshold: 3 (30s of failures before restart)
- Purpose: Recover from deadlocks, infinite loops

**Readiness Probe** (Service routing trigger):
- Checks if server can handle requests
- Initial delay: 5s (server starts quickly)
- Failure threshold: 3 (15s of failures before removal)
- Purpose: Prevent routing to overloaded/starting pods

**Pod Lifecycle**:

```
Pending → Image Pull → Creating → Running
                ↓ (if image not found)
            ImagePullBackOff (ISSUE #1)
                ↓ (if import fails)
            CrashLoopBackOff (ISSUE #2)
```

### 4. Docker Image

**Purpose**: Containerized MCP server application

**Entity**: `mcp-server:latest` image

**Build Context**: `phaseIV/backend/` (repository root/phaseIV/backend/)

**Image Layers**:
1. Base: `python:3.11-slim`
2. Dependencies: FastAPI, uvicorn, mcp-use, database clients
3. Application: `app/` directory with mcp_server and mcp_tools
4. Entry point: `mcp_server_entry.py`

**Directory Structure Inside Container**:
```
/app/
├── mcp_server_entry.py    # CMD entry point
├── app/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── server.py
│   │   └── config.py
│   └── mcp_tools/
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
└── requirements.txt
```

**Image Build Validation**:
- ✅ Python imports work: `from app.mcp_server.server import server`
- ✅ Entry point runs: `python mcp_server_entry.py`
- ✅ Server starts on port 8002
- ✅ Health endpoints respond

### 5. ConfigMap (Optional Future Enhancement)

**Purpose**: Externalize configuration without rebuilding image

**Not Currently Used**: Configuration via environment variables in Deployment

**Potential Use Cases**:
- Tool configuration (REGISTERED_TOOLS list)
- Server instructions text
- Retry/timeout policies

## Resource Relationships

```
Deployment (mcp-server)
  ├─ manages → ReplicaSet
  │              ├─ creates → Pod #1 (mcp-server-xxxxx-yyyyy)
  │              └─ creates → Pod #2 (mcp-server-xxxxx-zzzzz)
  │
  └─ template defines → Pod Spec
                          ├─ uses → Image (mcp-server:latest)
                          └─ exposes → Port 8002

Service (mcp-server)
  ├─ selects → Pods with label (app: mcp-server)
  ├─ exposes → Port 8002 (Service)
  ├─ targets → Port 8002 (Container)
  └─ provides DNS → mcp-server.todo-chatbot.svc.cluster.local

Image (mcp-server:latest)
  ├─ built from → phaseIV/backend/
  ├─ loaded via → minikube image load
  └─ pulled by → kubelet (with IfNotPresent policy)
```

## Constraints and Validation Rules

### Deployment Constraints

1. **Namespace Existence**: `todo-chatbot` namespace must exist before deployment
2. **Image Availability**: `mcp-server:latest` must be loaded in Minikube
3. **Port Availability**: Port 8002 must not be used by other services
4. **Resource Quotas**: Total resources (200m CPU, 256Mi RAM × 2) must fit namespace quota

### Service Constraints

1. **Selector Match**: Service selector must match Deployment pod labels exactly
2. **Port Uniqueness**: Port 8002 must be unique within namespace
3. **Type Restriction**: ClusterIP only (no external LoadBalancer needed)

### Pod Constraints

1. **Health Endpoints**: `/health` and `/ready` must respond with HTTP 200
2. **Startup Time**: Must pass readiness probe within 5s + 3×5s = 20s maximum
3. **Memory Limit**: Must not exceed 256Mi or pod will be OOMKilled
4. **CPU Throttling**: Can use up to 200m CPU, throttled beyond that

### Image Constraints

1. **Build Context**: Must build from backend root to preserve `app/` structure
2. **Entry Point**: Must use `mcp_server_entry.py` to avoid ImportError
3. **Port Exposure**: Must expose port 8002 in Dockerfile
4. **Base Image**: Must use Python 3.11 compatible base image

## Edge Case Handling

| Scenario | Current Behavior | Desired Behavior |
|----------|------------------|------------------|
| Image not in Minikube | ImagePullBackOff | Clear error + docs on `minikube image load` |
| ImportError on start | CrashLoopBackOff | Fixed via correct Dockerfile CMD |
| Port 8002 in use | Pod fails to start | Pre-deployment validation check |
| Readiness probe fails | Pod not added to service | Logs visible via `kubectl logs` |
| Liveness probe fails | Pod restarted | Alert + investigate root cause |
| Memory exceeds 256Mi | OOMKilled, pod restart | Monitor + adjust limits if needed |
| No pods ready | Service has no endpoints | Backend gets connection refused |

## Deployment Verification

**Required Checks After Deployment**:

1. **Pods Running**: `kubectl get pods -n todo-chatbot | grep mcp-server`
   - Expected: 2 pods with status `Running` and `2/2` ready

2. **Service Endpoints**: `kubectl get endpoints -n todo-chatbot mcp-server`
   - Expected: 2 pod IPs listed

3. **Health Check**: `kubectl exec -n todo-chatbot <backend-pod> -- curl http://mcp-server:8002/health`
   - Expected: HTTP 200 response

4. **Logs Clean**: `kubectl logs -n todo-chatbot deployment/mcp-server`
   - Expected: No ImportError, server started messages

## Summary

This deployment uses standard Kubernetes patterns:
- **Deployment** for replica management and rolling updates
- **Service** for stable DNS and load balancing
- **Probes** for health monitoring and traffic routing
- **Resource limits** for multi-tenancy and stability

Critical fix requirements:
- ✅ Image must be present in Minikube (`minikube image load`)
- ✅ Dockerfile must use correct build context (backend root)
- ✅ CMD must avoid relative import errors (use entry point)
- ✅ Health endpoints must respond for probes to pass
