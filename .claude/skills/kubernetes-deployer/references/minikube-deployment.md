# Minikube Deployment

Comprehensive guide to local Kubernetes deployment and testing with Minikube.

## Table of Contents

- [Minikube Setup](#minikube-setup)
- [Local Development Workflow](#local-development-workflow)
- [Image Management](#image-management)
- [Service Access](#service-access)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Advanced Features](#advanced-features)

---

## Minikube Setup

### Installation

**macOS:**
```bash
brew install minikube
```

**Linux:**
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Windows:**
```powershell
choco install minikube
# or
winget install Kubernetes.minikube
```

### Start Minikube

```bash
# Start with default settings
minikube start

# Start with specific driver
minikube start --driver=docker
minikube start --driver=virtualbox
minikube start --driver=hyperkit

# Start with custom resources
minikube start --cpus=4 --memory=8192 --disk-size=50g

# Start with specific Kubernetes version
minikube start --kubernetes-version=v1.28.0

# Start with multiple nodes
minikube start --nodes=3
```

### Verify Installation

```bash
# Check status
minikube status

# Check version
minikube version

# Get cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes
```

### Stop and Delete

```bash
# Stop Minikube
minikube stop

# Delete cluster
minikube delete

# Delete all clusters
minikube delete --all
```

---

## Local Development Workflow

### Complete Workflow Example

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Build Docker image
docker build -t myapp:latest .

# 4. Load image into Minikube
minikube image load myapp:latest

# 5. Create namespace
kubectl create namespace myapp

# 6. Deploy application
kubectl apply -f kubernetes/ -n myapp

# 7. Check deployment
kubectl get all -n myapp

# 8. Access service
minikube service myapp-service -n myapp

# 9. View logs
kubectl logs -n myapp -l app=myapp -f

# 10. Make changes and update
docker build -t myapp:v2 .
minikube image load myapp:v2
kubectl set image deployment/myapp myapp=myapp:v2 -n myapp
kubectl rollout status deployment/myapp -n myapp
```

### Using Minikube Docker Daemon

Instead of loading images, use Minikube's Docker daemon directly:

```bash
# Point Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Now build images directly in Minikube
docker build -t myapp:latest .

# Verify image is in Minikube
minikube image ls | grep myapp

# Deploy (no need to load image)
kubectl apply -f kubernetes/

# Reset to host Docker daemon
eval $(minikube docker-env -u)
```

### Hot Reload Development

**Option 1: Using kubectl port-forward**
```bash
# Forward port to local machine
kubectl port-forward deployment/myapp 3000:3000

# Access at http://localhost:3000
# Make code changes, rebuild, and redeploy
```

**Option 2: Using Skaffold**
```bash
# Install Skaffold
brew install skaffold

# Create skaffold.yaml
cat > skaffold.yaml <<EOF
apiVersion: skaffold/v4beta6
kind: Config
build:
  artifacts:
  - image: myapp
    docker:
      dockerfile: Dockerfile
  local:
    push: false
deploy:
  kubectl:
    manifests:
    - kubernetes/*.yaml
EOF

# Run with auto-rebuild
skaffold dev
```

---

## Image Management

### Load Images

```bash
# Load single image
minikube image load myapp:latest

# Load from tar
docker save myapp:latest | minikube image load -

# Load multiple images
minikube image load myapp:latest postgres:15 redis:7
```

### List Images

```bash
# List all images in Minikube
minikube image ls

# Filter images
minikube image ls | grep myapp
```

### Remove Images

```bash
# Remove specific image
minikube image rm myapp:latest

# Remove multiple images
minikube image rm myapp:latest myapp:v1
```

### Build Images in Minikube

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build image
docker build -t myapp:latest .

# Verify
docker images | grep myapp

# Deploy with imagePullPolicy: Never or IfNotPresent
kubectl apply -f deployment.yaml
```

---

## Service Access

### Access Methods

**1. minikube service**
```bash
# Open service in browser
minikube service myapp-service

# Get service URL
minikube service myapp-service --url

# Access in specific namespace
minikube service myapp-service -n myapp

# List all services
minikube service list
```

**2. kubectl port-forward**
```bash
# Forward service port
kubectl port-forward service/myapp-service 8080:80

# Forward deployment port
kubectl port-forward deployment/myapp 8080:3000

# Forward pod port
kubectl port-forward pod/myapp-abc123 8080:3000

# Access at http://localhost:8080
```

**3. NodePort**
```bash
# Get Minikube IP
minikube ip

# Get NodePort
kubectl get service myapp-service -o jsonpath='{.spec.ports[0].nodePort}'

# Access at http://<minikube-ip>:<node-port>
```

**4. Ingress**
```bash
# Enable ingress addon
minikube addons enable ingress

# Get ingress address
kubectl get ingress

# Add to /etc/hosts
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts

# Access at http://myapp.local
```

### Tunnel for LoadBalancer

```bash
# Start tunnel (requires sudo)
minikube tunnel

# In another terminal, check external IP
kubectl get service myapp-service

# Access service via external IP
curl http://<external-ip>
```

---

## Debugging and Troubleshooting

### Check Pod Status

```bash
# Get pods
kubectl get pods

# Get pods with more details
kubectl get pods -o wide

# Watch pods
kubectl get pods -w

# Get pods in all namespaces
kubectl get pods --all-namespaces
```

### View Logs

```bash
# View pod logs
kubectl logs myapp-abc123

# Follow logs
kubectl logs -f myapp-abc123

# View logs from all pods with label
kubectl logs -l app=myapp -f

# View previous container logs (after crash)
kubectl logs myapp-abc123 --previous

# View logs from specific container in pod
kubectl logs myapp-abc123 -c myapp

# Tail last 100 lines
kubectl logs myapp-abc123 --tail=100
```

### Describe Resources

```bash
# Describe pod (shows events)
kubectl describe pod myapp-abc123

# Describe deployment
kubectl describe deployment myapp

# Describe service
kubectl describe service myapp-service

# Describe node
kubectl describe node minikube
```

### Execute Commands in Pod

```bash
# Open shell in pod
kubectl exec -it myapp-abc123 -- /bin/sh

# Run single command
kubectl exec myapp-abc123 -- ls -la

# Run command in specific container
kubectl exec -it myapp-abc123 -c myapp -- /bin/bash

# Copy files to/from pod
kubectl cp myapp-abc123:/app/logs/app.log ./app.log
kubectl cp ./config.json myapp-abc123:/app/config.json
```

### Common Issues

**Issue: ImagePullBackOff**
```bash
# Problem: Kubernetes can't pull image
# Solution: Load image into Minikube
minikube image load myapp:latest

# Or use Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t myapp:latest .

# Ensure imagePullPolicy is correct
# imagePullPolicy: IfNotPresent  # or Never for local images
```

**Issue: CrashLoopBackOff**
```bash
# Check logs for errors
kubectl logs myapp-abc123

# Check previous logs
kubectl logs myapp-abc123 --previous

# Describe pod for events
kubectl describe pod myapp-abc123

# Common causes:
# - Application crashes on startup
# - Missing environment variables
# - Port conflicts
# - Health check failures
```

**Issue: Pending Pods**
```bash
# Check why pod is pending
kubectl describe pod myapp-abc123

# Common causes:
# - Insufficient resources
# - PVC not bound
# - Node selector mismatch

# Check node resources
kubectl top nodes
kubectl describe node minikube
```

**Issue: Service Not Accessible**
```bash
# Check service
kubectl get service myapp-service

# Check endpoints
kubectl get endpoints myapp-service

# Verify pod labels match service selector
kubectl get pods --show-labels
kubectl describe service myapp-service

# Test from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://myapp-service
```

### Resource Monitoring

```bash
# Enable metrics-server
minikube addons enable metrics-server

# View node resources
kubectl top nodes

# View pod resources
kubectl top pods

# View pod resources in namespace
kubectl top pods -n myapp

# Watch resource usage
watch kubectl top pods
```

### Dashboard

```bash
# Enable dashboard
minikube addons enable dashboard

# Open dashboard
minikube dashboard

# Get dashboard URL
minikube dashboard --url
```

---

## Advanced Features

### Addons

```bash
# List available addons
minikube addons list

# Enable addon
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard
minikube addons enable registry

# Disable addon
minikube addons disable ingress

# Common addons:
# - ingress: NGINX Ingress Controller
# - metrics-server: Resource metrics
# - dashboard: Kubernetes Dashboard
# - registry: Local Docker registry
# - storage-provisioner: Dynamic volume provisioning
```

### Local Registry

```bash
# Enable registry addon
minikube addons enable registry

# Get registry address
kubectl get service -n kube-system registry

# Tag and push image
docker tag myapp:latest localhost:5000/myapp:latest
docker push localhost:5000/myapp:latest

# Use in deployment
# image: localhost:5000/myapp:latest
```

### Multi-Node Cluster

```bash
# Start with multiple nodes
minikube start --nodes=3

# Check nodes
kubectl get nodes

# Label nodes
kubectl label node minikube-m02 node-role=worker
kubectl label node minikube-m03 node-role=worker

# Deploy with node affinity
# nodeSelector:
#   node-role: worker
```

### Profiles

```bash
# Create new profile
minikube start -p dev-cluster

# List profiles
minikube profile list

# Switch profile
minikube profile dev-cluster

# Delete profile
minikube delete -p dev-cluster
```

### Persistent Storage

```bash
# Create PVC
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
EOF

# Check PVC
kubectl get pvc

# Use in deployment
# volumeMounts:
# - name: data
#   mountPath: /data
# volumes:
# - name: data
#   persistentVolumeClaim:
#     claimName: myapp-pvc
```

### SSH into Minikube

```bash
# SSH into Minikube VM
minikube ssh

# Run commands
docker ps
ls /var/lib/minikube

# Exit
exit
```

### Mount Host Directory

```bash
# Mount host directory into Minikube
minikube mount /path/on/host:/path/in/minikube

# Use in pod
# volumeMounts:
# - name: host-mount
#   mountPath: /data
# volumes:
# - name: host-mount
#   hostPath:
#     path: /path/in/minikube
```

---

## Complete Example: Deploy Full Stack App

### 1. Prepare Application

**Dockerfile:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "server.js"]
```

**kubernetes/deployment.yaml:**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: myapp

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: myapp
data:
  NODE_ENV: "production"
  DATABASE_HOST: "postgres"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: myapp
type: Opaque
stringData:
  DATABASE_PASSWORD: "changeme"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 3000
        envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: myapp
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
    nodePort: 30080
```

### 2. Deploy to Minikube

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build image
docker build -t myapp:latest .

# Verify image
docker images | grep myapp

# Deploy
kubectl apply -f kubernetes/deployment.yaml

# Check status
kubectl get all -n myapp

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=myapp -n myapp --timeout=60s

# View logs
kubectl logs -n myapp -l app=myapp

# Access service
minikube service myapp-service -n myapp

# Or get URL
minikube service myapp-service -n myapp --url

# Test endpoint
curl $(minikube service myapp-service -n myapp --url)/health
```

### 3. Update Application

```bash
# Make code changes
# ...

# Rebuild image
docker build -t myapp:v2 .

# Update deployment
kubectl set image deployment/myapp myapp=myapp:v2 -n myapp

# Watch rollout
kubectl rollout status deployment/myapp -n myapp

# Check new pods
kubectl get pods -n myapp

# Rollback if needed
kubectl rollout undo deployment/myapp -n myapp
```

### 4. Debug Issues

```bash
# Check pod status
kubectl get pods -n myapp

# View logs
kubectl logs -n myapp -l app=myapp -f

# Describe pod
kubectl describe pod -n myapp <pod-name>

# Execute commands in pod
kubectl exec -it -n myapp <pod-name> -- /bin/sh

# Check service
kubectl get service -n myapp
kubectl describe service myapp-service -n myapp

# Check endpoints
kubectl get endpoints -n myapp
```

### 5. Cleanup

```bash
# Delete resources
kubectl delete namespace myapp

# Or delete specific resources
kubectl delete -f kubernetes/deployment.yaml

# Stop Minikube
minikube stop

# Delete cluster
minikube delete
```

---

## Best Practices

### 1. Use Namespaces

```bash
# Create namespace
kubectl create namespace dev

# Deploy to namespace
kubectl apply -f deployment.yaml -n dev

# Set default namespace
kubectl config set-context --current --namespace=dev
```

### 2. Resource Limits

Always set resource requests and limits:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### 3. Health Checks

Implement liveness and readiness probes:
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 4. Image Pull Policy

For local development:
```yaml
imagePullPolicy: Never  # or IfNotPresent
```

### 5. Labels and Selectors

Use consistent labels:
```yaml
metadata:
  labels:
    app: myapp
    version: v1
    environment: dev
```

### 6. Configuration Management

Use ConfigMaps and Secrets:
```bash
# Create from file
kubectl create configmap app-config --from-file=config.json

# Create from literal
kubectl create secret generic app-secrets --from-literal=password=secret
```

---

## Quick Reference

### Essential Commands

```bash
# Cluster management
minikube start
minikube stop
minikube delete
minikube status

# Image management
minikube image load myapp:latest
minikube image ls
eval $(minikube docker-env)

# Service access
minikube service myapp-service
minikube service myapp-service --url
minikube tunnel

# Debugging
kubectl get pods
kubectl logs <pod-name> -f
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- /bin/sh

# Addons
minikube addons list
minikube addons enable ingress
minikube dashboard
```

### Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias k='kubectl'
alias kgp='kubectl get pods'
alias kgs='kubectl get services'
alias kgd='kubectl get deployments'
alias kl='kubectl logs -f'
alias kd='kubectl describe'
alias ke='kubectl exec -it'
alias mk='minikube'
```
