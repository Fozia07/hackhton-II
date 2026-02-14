# Health and Readiness Endpoints Contract

**Service**: MCP Server
**Base URL**: `http://mcp-server:8002` (within todo-chatbot namespace)
**Protocol**: HTTP/1.1
**Date**: 2026-02-13

## Overview

Health and readiness endpoints used by Kubernetes probes to manage pod lifecycle.

## Endpoints

### 1. Liveness Probe - GET /health

**Purpose**: Verify server process is alive and responding

**Request**:
```http
GET /health HTTP/1.1
Host: mcp-server:8002
```

**Success Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2026-02-13T10:30:00Z",
  "service": "todo-ai-chatbot-mcp-server",
  "version": "1.0.0"
}
```

**Failure Response** (503 Service Unavailable):
```json
{
  "status": "unhealthy",
  "timestamp": "2026-02-13T10:30:00Z",
  "error": "Server deadlock detected"
}
```

**Response Headers**:
```
Content-Type: application/json
Cache-Control: no-cache
```

**Timeout**: 5 seconds (configured in Deployment)

**Kubernetes Behavior**:
- Initial delay: 30 seconds (allows server startup)
- Check interval: Every 10 seconds
- Failure threshold: 3 consecutive failures → Pod restart
- Success threshold: 1 success → Pod marked healthy

**Error Scenarios**:
- Timeout (>5s) → Probe failure
- Non-200 status → Probe failure
- Connection refused → Probe failure (pod will restart)

---

### 2. Readiness Probe - GET /ready

**Purpose**: Verify server is ready to accept traffic

**Request**:
```http
GET /ready HTTP/1.1
Host: mcp-server:8002
```

**Success Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2026-02-13T10:30:00Z",
  "dependencies": {
    "database": "connected",
    "mcp_tools": "loaded"
  },
  "registered_tools": 5
}
```

**Not Ready Response** (503 Service Unavailable):
```json
{
  "status": "not_ready",
  "timestamp": "2026-02-13T10:30:00Z",
  "dependencies": {
    "database": "connecting",
    "mcp_tools": "loading"
  },
  "reason": "Database connection initializing"
}
```

**Response Headers**:
```
Content-Type: application/json
Cache-Control: no-cache
```

**Timeout**: 3 seconds (configured in Deployment)

**Kubernetes Behavior**:
- Initial delay: 5 seconds (server starts quickly)
- Check interval: Every 5 seconds
- Failure threshold: 3 consecutive failures → Pod removed from Service
- Success threshold: 1 success → Pod added to Service endpoints

**Readiness vs Liveness**:
- **Readiness**: Can temporarily fail (overload, dependency unavailable) → Remove from load balancer
- **Liveness**: Should only fail on deadlock/crash → Restart pod

**Error Scenarios**:
- Timeout (>3s) → Probe failure, pod removed from service
- Non-200 status → Probe failure, pod removed from service
- Connection refused → Probe failure, pod removed from service

---

## Implementation Requirements

### Option 1: mcp-use SDK Auto-Provisioning (PREFERRED)

**Check if mcp-use SDK provides health endpoints automatically**:
- Review mcp-use documentation
- Test startup to verify `/health` and `/ready` exist
- Verify response format matches Kubernetes expectations

**If auto-provisioned**: No code changes needed, just validation

### Option 2: Manual Implementation (FALLBACK)

**If mcp-use doesn't provide health endpoints**, add FastAPI routes:

```python
# In phaseIV/backend/app/mcp_server/health.py

from fastapi import FastAPI, Response
from datetime import datetime
import asyncio

app = FastAPI()

@app.get("/health")
async def liveness():
    """Liveness probe - checks if server process is alive"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "todo-ai-chatbot-mcp-server",
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness():
    """Readiness probe - checks if server can handle requests"""
    # Check dependencies (database, tools loaded)
    dependencies = {
        "database": "connected",  # TODO: Actual DB check
        "mcp_tools": "loaded"      # TODO: Verify tools registered
    }

    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dependencies": dependencies,
        "registered_tools": 5
    }
```

**Integration with MCP Server**:
- Option A: Run FastAPI alongside MCP server (separate port)
- Option B: MCP server SDK might support middleware/routes
- Option C: Use lightweight HTTP server just for health checks

## Testing

### Manual Testing

**From within cluster**:
```bash
# From backend pod
kubectl exec -n todo-chatbot <backend-pod> -- curl http://mcp-server:8002/health
kubectl exec -n todo-chatbot <backend-pod> -- curl http://mcp-server:8002/ready
```

**Expected output**:
```json
{"status":"healthy","timestamp":"2026-02-13T10:30:00Z",...}
```

### Kubernetes Probe Testing

**Watch probe status**:
```bash
kubectl describe pod -n todo-chatbot <mcp-server-pod>
```

**Look for**:
- `Liveness: http-get http://:8002/health delay=30s timeout=5s`
- `Readiness: http-get http://:8002/ready delay=5s timeout=3s`
- Events: `Liveness probe succeeded` / `Readiness probe succeeded`

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Liveness probe fails | `kubectl logs <pod>` shows errors | Check server startup, fix deadlocks |
| Readiness probe fails | Pod not in endpoints list | Check dependencies, increase timeout |
| Connection refused | Server not listening on 8002 | Verify PORT env var, check CMD |
| Timeout | Response takes >5s (liveness) or >3s (readiness) | Optimize endpoint, increase timeout |
| 404 Not Found | Endpoints not registered | Implement health routes |

## Monitoring

**Metrics to track**:
- Liveness probe success rate (should be ~100%)
- Readiness probe success rate (can dip during load)
- Average response time (<100ms ideal)
- Pod restart count (triggered by liveness failures)

**Alerts**:
- Alert if liveness probe fails >1 time in 5 minutes
- Alert if readiness probe fails for >30 seconds
- Alert if pod restart count increases

## Summary

Health endpoints are critical for Kubernetes pod lifecycle:
- **Liveness** (`/health`) → Determines if pod should be restarted
- **Readiness** (`/ready`) → Determines if pod should receive traffic

**Action Items**:
1. Verify if mcp-use SDK auto-provisions health endpoints
2. If not, implement FastAPI routes for /health and /ready
3. Test endpoints respond within timeout limits
4. Validate probe configuration in Deployment YAML
