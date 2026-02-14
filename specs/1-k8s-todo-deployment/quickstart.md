# Quickstart: Deploy Todo AI Chatbot to Minikube

**Feature**: Local Kubernetes Deployment of Todo AI Chatbot
**Estimated Time**: 5-10 minutes
**Prerequisites**: Minikube, kubectl, Helm, Docker images built

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Minikube installed and running
- [ ] kubectl installed and configured
- [ ] Helm 3.x installed
- [ ] Docker images built:
  - `phase4-frontend:latest`
  - `phase4-backend:latest`
- [ ] Minimum resources: 4GB RAM, 2 CPUs
- [ ] Internet connectivity (for Phase II auth service)

---

## Quick Deployment (5 Steps)

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192

# Verify cluster is running
minikube status
kubectl cluster-info
```

**Expected Output**:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

### Step 2: Load Docker Images

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Verify images exist
docker images | grep phase4

# Expected output:
# phase4-backend    latest    <image-id>    <time>    <size>
# phase4-frontend   latest    <image-id>    <time>    <size>
```

**If images don't exist**, build them first:
```bash
# Backend
cd backend
docker build -t phase4-backend:latest .

# Frontend
cd frontend
docker build -t phase4-frontend:latest .
```

---

### Step 3: Deploy with Helm

```bash
# Navigate to Helm chart directory
cd helm-charts/todo-chatbot

# Install the chart
helm install todo-chatbot . \
  --create-namespace \
  --namespace todo-chatbot

# Wait for deployment to complete
kubectl wait --for=condition=ready pod \
  -n todo-chatbot \
  -l app.kubernetes.io/instance=todo-chatbot \
  --timeout=120s
```

**Expected Output**:
```
NAME: todo-chatbot
LAST DEPLOYED: <timestamp>
NAMESPACE: todo-chatbot
STATUS: deployed
REVISION: 1
```

---

### Step 4: Verify Deployment

```bash
# Check pod status
kubectl get pods -n todo-chatbot

# Expected output:
# NAME                                    READY   STATUS    RESTARTS   AGE
# todo-chatbot-backend-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
# todo-chatbot-backend-xxxxxxxxxx-xxxxx   1/1     Running   0          30s
# todo-chatbot-frontend-xxxxxxxxxx-xxxxx  1/1     Running   0          30s
# todo-chatbot-frontend-xxxxxxxxxx-xxxxx  1/1     Running   0          30s

# Check services
kubectl get services -n todo-chatbot

# Expected output:
# NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# todo-chatbot-backend      ClusterIP   10.96.xxx.xxx   <none>        80/TCP         30s
# todo-chatbot-frontend     NodePort    10.96.xxx.xxx   <none>        80:30080/TCP   30s
```

---

### Step 5: Access Frontend

```bash
# Open frontend in browser
minikube service todo-chatbot-frontend -n todo-chatbot

# Or get the URL manually
export NODE_PORT=$(kubectl get --namespace todo-chatbot -o jsonpath="{.spec.ports[0].nodePort}" services todo-chatbot-frontend)
export NODE_IP=$(minikube ip)
echo "Frontend URL: http://$NODE_IP:$NODE_PORT"
```

**Expected**: Browser opens with Todo AI Chatbot interface

---

## Validation Tests

### Test 1: Backend Health Check

```bash
# Port forward to backend
kubectl port-forward -n todo-chatbot svc/todo-chatbot-backend 8000:80 &

# Test health endpoint
curl http://localhost:8000/health

# Expected output:
# {"status": "healthy"} or similar

# Stop port forward
kill %1
```

### Test 2: Frontend Accessibility

```bash
# Access frontend URL from Step 5
# Verify:
# - Page loads successfully
# - UI displays correctly
# - No console errors in browser DevTools
```

### Test 3: Frontend-Backend Communication

```bash
# In browser:
# 1. Open frontend URL
# 2. Open browser DevTools (F12)
# 3. Go to Network tab
# 4. Perform an action that requires backend (e.g., load todos)
# 5. Verify requests to backend succeed (200 OK)
```

### Test 4: End-to-End Authentication

```bash
# In browser:
# 1. Attempt to authenticate
# 2. Verify authentication request flows:
#    Frontend → Backend → Phase II Auth Service
# 3. Check for successful authentication response
```

### Test 5: Pod Resilience

```bash
# Delete a backend pod
kubectl delete pod -n todo-chatbot -l app.kubernetes.io/component=backend --field-selector=status.phase=Running | head -1

# Watch pod recreation
kubectl get pods -n todo-chatbot -w

# Verify:
# - New pod is created automatically
# - New pod reaches Running state
# - Service continues to work
```

### Test 6: Resource Usage

```bash
# Enable metrics-server if not already enabled
minikube addons enable metrics-server

# Wait a moment for metrics to be collected
sleep 30

# Check resource usage
kubectl top pods -n todo-chatbot

# Expected output (approximate):
# NAME                                    CPU(cores)   MEMORY(bytes)
# todo-chatbot-backend-xxx                50m          120Mi
# todo-chatbot-backend-xxx                50m          120Mi
# todo-chatbot-frontend-xxx               25m          60Mi
# todo-chatbot-frontend-xxx               25m          60Mi

# Verify usage is within limits:
# Backend: < 200m CPU, < 256Mi memory
# Frontend: < 100m CPU, < 128Mi memory
```

---

## Common Operations

### View Logs

```bash
# Backend logs
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=frontend -f

# Specific pod logs
kubectl logs -n todo-chatbot <pod-name> -f
```

### Scale Services

```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-chatbot-backend -n todo-chatbot --replicas=3

# Scale frontend to 1 replica
kubectl scale deployment todo-chatbot-frontend -n todo-chatbot --replicas=1

# Verify scaling
kubectl get pods -n todo-chatbot
```

### Update Configuration

```bash
# Update via Helm
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --namespace todo-chatbot \
  --set backend.replicaCount=3 \
  --set backend.env.LOG_LEVEL=debug

# Check rollout status
kubectl rollout status deployment/todo-chatbot-backend -n todo-chatbot
```

### Rollback Deployment

```bash
# View release history
helm history todo-chatbot -n todo-chatbot

# Rollback to previous version
helm rollback todo-chatbot -n todo-chatbot

# Rollback to specific revision
helm rollback todo-chatbot 1 -n todo-chatbot
```

---

## Troubleshooting

### Issue: Pods Not Starting

**Symptoms**: Pods stuck in `Pending`, `ImagePullBackOff`, or `CrashLoopBackOff`

**Diagnosis**:
```bash
# Check pod status
kubectl get pods -n todo-chatbot

# Describe problematic pod
kubectl describe pod -n todo-chatbot <pod-name>

# Check pod logs
kubectl logs -n todo-chatbot <pod-name>
```

**Common Causes & Solutions**:

1. **ImagePullBackOff**: Images not in Minikube
   ```bash
   eval $(minikube docker-env)
   docker images | grep phase4
   # If missing, rebuild images
   ```

2. **CrashLoopBackOff**: Application error
   ```bash
   kubectl logs -n todo-chatbot <pod-name> --previous
   # Check for application errors in logs
   ```

3. **Pending**: Insufficient resources
   ```bash
   kubectl describe node minikube
   # Check available resources
   # Restart Minikube with more resources if needed
   ```

---

### Issue: Service Not Accessible

**Symptoms**: Cannot access frontend URL, connection refused

**Diagnosis**:
```bash
# Check service
kubectl get service -n todo-chatbot todo-chatbot-frontend

# Check endpoints
kubectl get endpoints -n todo-chatbot todo-chatbot-frontend

# Check Minikube service list
minikube service list
```

**Solutions**:

1. **No endpoints**: Pods not ready
   ```bash
   kubectl get pods -n todo-chatbot
   # Wait for pods to be Running and Ready
   ```

2. **Wrong URL**: Get correct URL
   ```bash
   minikube service todo-chatbot-frontend -n todo-chatbot --url
   ```

3. **Minikube tunnel needed**: For LoadBalancer type
   ```bash
   minikube tunnel
   ```

---

### Issue: Backend Cannot Reach Phase II Auth Service

**Symptoms**: Authentication fails, backend logs show connection errors

**Diagnosis**:
```bash
# Check backend logs
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=backend

# Test connectivity from pod
kubectl exec -n todo-chatbot <backend-pod-name> -- \
  curl -I https://fozi07-todo-full-stack-app.hf.space
```

**Solutions**:

1. **Network connectivity**: Verify internet access
   ```bash
   # From host machine
   curl -I https://fozi07-todo-full-stack-app.hf.space
   ```

2. **Firewall/proxy**: Check network restrictions

3. **Service down**: Verify Phase II service is operational

---

### Issue: High Resource Usage

**Symptoms**: Pods using more resources than expected, OOMKilled

**Diagnosis**:
```bash
# Check resource usage
kubectl top pods -n todo-chatbot

# Check pod events
kubectl describe pod -n todo-chatbot <pod-name>
```

**Solutions**:

1. **Increase limits**:
   ```bash
   helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
     --namespace todo-chatbot \
     --set backend.resources.limits.memory=512Mi
   ```

2. **Reduce replicas**:
   ```bash
   helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
     --namespace todo-chatbot \
     --set backend.replicaCount=1
   ```

---

## Cleanup

### Uninstall Deployment

```bash
# Uninstall Helm release
helm uninstall todo-chatbot -n todo-chatbot

# Delete namespace
kubectl delete namespace todo-chatbot

# Verify cleanup
kubectl get all -n todo-chatbot
# Should return: No resources found
```

### Stop Minikube

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster (optional)
minikube delete
```

---

## Next Steps

After successful deployment:

1. **Explore the application**: Test all features in the UI
2. **Monitor performance**: Use `kubectl top` to track resource usage
3. **Test resilience**: Delete pods and verify automatic recovery
4. **Experiment with scaling**: Try different replica counts
5. **Review logs**: Understand application behavior
6. **Test updates**: Practice Helm upgrades and rollbacks
7. **Document issues**: Note any problems encountered

---

## Quick Reference

### Essential Commands

```bash
# Deployment
helm install todo-chatbot ./helm-charts/todo-chatbot -n todo-chatbot --create-namespace

# Status
kubectl get all -n todo-chatbot
helm status todo-chatbot -n todo-chatbot

# Logs
kubectl logs -n todo-chatbot -l app.kubernetes.io/component=backend -f

# Access
minikube service todo-chatbot-frontend -n todo-chatbot

# Update
helm upgrade todo-chatbot ./helm-charts/todo-chatbot -n todo-chatbot

# Cleanup
helm uninstall todo-chatbot -n todo-chatbot
```

### Useful Aliases

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias k='kubectl'
alias kgp='kubectl get pods -n todo-chatbot'
alias kgs='kubectl get services -n todo-chatbot'
alias kl='kubectl logs -n todo-chatbot'
alias kd='kubectl describe -n todo-chatbot'
alias h='helm'
alias hl='helm list -n todo-chatbot'
alias mk='minikube'
```

---

## Support

For additional help:
- **Detailed Plan**: `specs/1-k8s-todo-deployment/plan.md`
- **Helm Chart Design**: `specs/1-k8s-todo-deployment/helm-chart-design.md`
- **Configuration Contracts**: `specs/1-k8s-todo-deployment/contracts/`
- **Troubleshooting Guide**: (to be created during implementation)

---

**Quickstart Status**: ✅ Complete - Ready for deployment
