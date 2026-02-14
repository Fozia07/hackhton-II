# MCP Server Deployment Quickstart

**Feature**: Fix MCP Server Deployment Issues
**Environment**: Minikube (local Kubernetes)
**Namespace**: `todo-chatbot`
**Date**: 2026-02-13

## Prerequisites

- ✅ Minikube installed and running
- ✅ kubectl configured for Minikube context
- ✅ Docker installed on host machine
- ✅ Repository cloned at `C:\Users\Fozia\hackhton-spec\hackhton-II`

## Quick Start (5 Minutes)

### Step 1: Build Docker Image

```bash
cd phaseIV/backend

# Build MCP server image with correct build context
docker build -f Dockerfile.mcp -t mcp-server:latest .
```

**Expected Output**:
```
Successfully built <image-id>
Successfully tagged mcp-server:latest
```

**Verify Image**:
```bash
docker images | grep mcp-server
```

Expected: `mcp-server   latest   <image-id>   <timestamp>   XXX MB`

---

### Step 2: Load Image into Minikube

```bash
# Transfer image from host Docker to Minikube
minikube image load mcp-server:latest
```

**Expected Output**:
```
Loading image 'mcp-server:latest' to minikube...
```

**Verify in Minikube**:
```bash
minikube image ls | grep mcp-server
```

Expected: `docker.io/library/mcp-server:latest`

**Alternative Method** (build directly in Minikube):
```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build image (now builds inside Minikube)
cd phaseIV/backend
docker build -f Dockerfile.mcp -t mcp-server:latest .

# Switch back to host Docker daemon
eval $(minikube docker-env -u)
```

---

### Step 3: Create Namespace (if not exists)

```bash
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -
```

**Expected Output**:
```
namespace/todo-chatbot created
```
or
```
namespace/todo-chatbot unchanged
```

---

### Step 4: Deploy MCP Server

```bash
cd ../..  # Return to repository root

# Apply Deployment and Service
kubectl apply -f mcp-server-deployment.yaml
```

**Expected Output**:
```
deployment.apps/mcp-server created
service/mcp-server created
```

---

### Step 5: Verify Deployment

**Check Pods Status**:
```bash
kubectl get pods -n todo-chatbot -l app=mcp-server
```

**Expected Output** (wait 30-60 seconds):
```
NAME                          READY   STATUS    RESTARTS   AGE
mcp-server-xxxxx-yyyyy        2/2     Running   0          45s
mcp-server-xxxxx-zzzzz        2/2     Running   0          45s
```

**Troubleshooting Pod Issues**:

| Status | Meaning | Solution |
|--------|---------|----------|
| `ImagePullBackOff` | Image not in Minikube | Repeat Step 2: `minikube image load` |
| `CrashLoopBackOff` | Container starts then crashes | Check logs: `kubectl logs -n todo-chatbot <pod-name>` |
| `Pending` | Waiting for resources | Check events: `kubectl describe pod -n todo-chatbot <pod-name>` |
| `ContainerCreating` | Normal startup state | Wait 10-20 seconds |

---

### Step 6: Check Service

```bash
kubectl get svc -n todo-chatbot mcp-server
```

**Expected Output**:
```
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
mcp-server   ClusterIP   10.96.xxx.xxx   <none>        8002/TCP   1m
```

**Check Service Endpoints**:
```bash
kubectl get endpoints -n todo-chatbot mcp-server
```

**Expected Output** (2 pod IPs):
```
NAME         ENDPOINTS                         AGE
mcp-server   172.17.0.x:8002,172.17.0.y:8002   1m
```

---

### Step 7: Test Health Endpoints

**From within cluster** (requires backend pod):
```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pods -n todo-chatbot -l app=todo-chatbot-backend -o jsonpath='{.items[0].metadata.name}')

# Test health endpoint
kubectl exec -n todo-chatbot $BACKEND_POD -- curl -s http://mcp-server:8002/health

# Test readiness endpoint
kubectl exec -n todo-chatbot $BACKEND_POD -- curl -s http://mcp-server:8002/ready
```

**Expected Response**:
```json
{"status":"healthy","timestamp":"2026-02-13T10:30:00Z","service":"todo-ai-chatbot-mcp-server"}
```

**If backend pod not available**, use port-forward:
```bash
# Forward MCP server port to localhost
kubectl port-forward -n todo-chatbot svc/mcp-server 8002:8002

# In another terminal, test locally
curl http://localhost:8002/health
```

---

### Step 8: Test MCP Tool Listing

```bash
# From backend pod
kubectl exec -n todo-chatbot $BACKEND_POD -- curl -X POST http://mcp-server:8002/ \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

**Expected Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {"name": "add_task", ...},
      {"name": "list_tasks", ...},
      {"name": "complete_task", ...},
      {"name": "delete_task", ...},
      {"name": "update_task", ...}
    ]
  }
}
```

---

## Verification Checklist

- [ ] Docker image `mcp-server:latest` built successfully
- [ ] Image loaded into Minikube
- [ ] Namespace `todo-chatbot` exists
- [ ] 2 MCP server pods in `Running` state with `2/2` ready
- [ ] Service `mcp-server` has 2 endpoints
- [ ] Health endpoint `/health` returns HTTP 200
- [ ] Readiness endpoint `/ready` returns HTTP 200
- [ ] MCP tools list endpoint returns 5 tools
- [ ] No `ImagePullBackOff` errors
- [ ] No `CrashLoopBackOff` errors
- [ ] Pod logs show "Starting MCP Server" message

---

## Common Issues and Solutions

### Issue 1: ImagePullBackOff

**Symptoms**:
```bash
kubectl get pods -n todo-chatbot
# Shows: ImagePullBackOff or ErrImagePull
```

**Diagnosis**:
```bash
kubectl describe pod -n todo-chatbot <pod-name> | grep -A 5 "Events:"
# Shows: Failed to pull image "mcp-server:latest"
```

**Solutions**:
1. **Verify image exists on host**:
   ```bash
   docker images | grep mcp-server
   ```

2. **Load image into Minikube**:
   ```bash
   minikube image load mcp-server:latest
   ```

3. **Verify in Minikube**:
   ```bash
   minikube ssh docker images | grep mcp-server
   ```

4. **Restart deployment**:
   ```bash
   kubectl rollout restart deployment/mcp-server -n todo-chatbot
   ```

---

### Issue 2: CrashLoopBackOff (ImportError)

**Symptoms**:
```bash
kubectl get pods -n todo-chatbot
# Shows: CrashLoopBackOff
```

**Diagnosis**:
```bash
kubectl logs -n todo-chatbot <pod-name>
# Shows: ImportError: attempted relative import with no known parent package
```

**Root Cause**: Dockerfile CMD uses incorrect entry point or build context

**Solutions**:
1. **Verify Dockerfile.mcp CMD**:
   ```dockerfile
   CMD ["python", "mcp_server_entry.py"]
   ```

2. **Verify build context**:
   ```bash
   cd phaseIV/backend
   docker build -f Dockerfile.mcp -t mcp-server:latest .
   # Must build from phaseIV/backend, not from app/mcp_server
   ```

3. **Rebuild and reload**:
   ```bash
   docker build -f Dockerfile.mcp -t mcp-server:latest .
   minikube image load mcp-server:latest
   kubectl rollout restart deployment/mcp-server -n todo-chatbot
   ```

---

### Issue 3: Pods Not Ready (Probe Failures)

**Symptoms**:
```bash
kubectl get pods -n todo-chatbot
# Shows: Running but 1/2 or 0/2 ready
```

**Diagnosis**:
```bash
kubectl describe pod -n todo-chatbot <pod-name> | grep -A 10 "Conditions:"
# Shows: Readiness probe failed: Get "http://...health": dial tcp: connection refused
```

**Solutions**:
1. **Check if server started**:
   ```bash
   kubectl logs -n todo-chatbot <pod-name>
   # Should show: "Starting MCP Server"
   ```

2. **Verify port 8002 listening**:
   ```bash
   kubectl exec -n todo-chatbot <pod-name> -- netstat -tuln | grep 8002
   ```

3. **Check health endpoint exists**:
   ```bash
   kubectl exec -n todo-chatbot <pod-name> -- curl http://localhost:8002/health
   ```

4. **If health endpoints missing**, implement them (see contracts/health-endpoints.md)

---

### Issue 4: Service Connection Refused

**Symptoms**: Backend pod cannot reach `http://mcp-server:8002`

**Diagnosis**:
```bash
kubectl exec -n todo-chatbot $BACKEND_POD -- curl -v http://mcp-server:8002/health
# Shows: Connection refused
```

**Solutions**:
1. **Check service endpoints**:
   ```bash
   kubectl get endpoints -n todo-chatbot mcp-server
   # Should show pod IPs, not <none>
   ```

2. **Check pods are ready**:
   ```bash
   kubectl get pods -n todo-chatbot -l app=mcp-server
   # Should show 2/2 READY
   ```

3. **Test DNS resolution**:
   ```bash
   kubectl exec -n todo-chatbot $BACKEND_POD -- nslookup mcp-server
   # Should resolve to ClusterIP
   ```

4. **Verify service selector**:
   ```bash
   kubectl get svc -n todo-chatbot mcp-server -o yaml | grep selector
   # Should match pod labels: app: mcp-server
   ```

---

## Monitoring and Logs

### View Logs

**All MCP server pods**:
```bash
kubectl logs -n todo-chatbot -l app=mcp-server --tail=50 -f
```

**Specific pod**:
```bash
kubectl logs -n todo-chatbot <pod-name> -f
```

**Previous crashed container**:
```bash
kubectl logs -n todo-chatbot <pod-name> --previous
```

### Watch Pod Status

```bash
watch kubectl get pods -n todo-chatbot -l app=mcp-server
```

### Describe Pod (detailed status)

```bash
kubectl describe pod -n todo-chatbot <pod-name>
```

Look for:
- **Events**: Shows probe successes/failures, restarts, scheduling
- **Conditions**: Ready, ContainersReady, PodScheduled
- **Status**: Running, Pending, Failed

---

## Cleanup (Optional)

**Remove deployment**:
```bash
kubectl delete -f mcp-server-deployment.yaml
```

**Remove namespace** (deletes all resources):
```bash
kubectl delete namespace todo-chatbot
```

**Remove Docker image from Minikube**:
```bash
minikube ssh docker rmi mcp-server:latest
```

**Remove Docker image from host**:
```bash
docker rmi mcp-server:latest
```

---

## Next Steps

After successful deployment:

1. ✅ **Integrate with backend service** - Update chatbot routes to call MCP tools
2. ✅ **Add monitoring** - Set up Prometheus metrics for MCP server
3. ✅ **Configure alerts** - Alert on pod restarts, probe failures
4. ✅ **Test end-to-end** - Verify chatbot can create/list/complete tasks
5. ✅ **Document runbook** - Operations guide for production issues

---

## Reference Commands

### Quick Status Check
```bash
# One-liner to check entire deployment
kubectl get all -n todo-chatbot -l app=mcp-server
```

### Port Forward for Local Testing
```bash
kubectl port-forward -n todo-chatbot svc/mcp-server 8002:8002
# Access at http://localhost:8002
```

### Restart Deployment
```bash
kubectl rollout restart deployment/mcp-server -n todo-chatbot
```

### Scale Replicas
```bash
kubectl scale deployment/mcp-server -n todo-chatbot --replicas=3
```

### View Resource Usage
```bash
kubectl top pods -n todo-chatbot -l app=mcp-server
```

---

## Summary

This quickstart deploys the MCP server to Minikube in 5 steps:
1. Build Docker image with correct context
2. Load image into Minikube
3. Create namespace
4. Deploy via kubectl apply
5. Verify pods running and healthy

**Success Criteria**: 2 pods running, health checks passing, backend can reach `http://mcp-server:8002`
