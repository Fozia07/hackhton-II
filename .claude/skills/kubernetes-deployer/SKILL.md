---
name: kubernetes-deployer
description: |
  Package and deploy applications to Kubernetes with Dockerfiles, Helm charts, and local Minikube deployment.
  Use when containerizing applications, creating Kubernetes manifests, setting up Helm charts, deploying to Minikube,
  or preparing cloud-ready configurations. Focuses on local-first deployment with stateless services.
  Handles Docker image building, Kubernetes resource definitions, Helm templating, and local testing workflows.
---

# Kubernetes Deployer

Package and deploy applications to Kubernetes from Docker images to production-ready Helm charts.

## What This Skill Does

- Creates optimized Dockerfiles for various application types
- Builds and manages Docker images with best practices
- Generates Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Creates Helm charts with templating and values management
- Deploys applications to local Minikube for testing
- Implements health checks, resource limits, and scaling configurations
- Sets up ingress, persistent volumes, and networking
- Provides local-first development workflows

## What This Skill Does NOT Do

- Manage cloud provider-specific infrastructure (EKS, GKE, AKS)
- Handle CI/CD pipeline configuration (GitHub Actions, Jenkins)
- Manage production cluster operations (monitoring, logging aggregation)
- Configure service mesh implementations (Istio, Linkerd)
- Handle stateful applications with complex data persistence requirements

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Application type, dependencies, build process, existing Docker/K8s files |
| **Conversation** | User's requirements: app type, environment variables, ports, scaling needs |
| **Skill References** | Docker patterns, Kubernetes manifests, Helm charts, Minikube workflows |
| **User Guidelines** | Team conventions, security requirements, resource constraints |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Core Architecture

### How Kubernetes Deployment Works

```
Application Code
    ↓
Dockerfile (Build Instructions)
    ↓
Docker Image (Containerized App)
    ↓
Kubernetes Manifest / Helm Chart
    ↓
Minikube / Kubernetes Cluster
    ↓
Running Pods (Containers)
    ↓
Service (Load Balancing)
    ↓
Ingress (External Access)
```

### Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Dockerfile** | Container image definition | Docker |
| **Deployment** | Pod management and scaling | Kubernetes |
| **Service** | Internal load balancing | Kubernetes |
| **ConfigMap** | Configuration management | Kubernetes |
| **Secret** | Sensitive data storage | Kubernetes |
| **Ingress** | External HTTP/HTTPS routing | Kubernetes + Ingress Controller |
| **Helm Chart** | Package manager for K8s | Helm |
| **Minikube** | Local Kubernetes cluster | Minikube |

---

## Implementation Levels

Progressive complexity for different use cases:

| Level | Capability | When to Use |
|-------|-----------|-------------|
| **Simple Container** | Basic Dockerfile + single pod | Learning, prototyping |
| **Basic Deployment** | Deployment + Service | Simple stateless apps |
| **With Configuration** | ConfigMaps + Secrets | Apps with environment config |
| **Helm Chart** | Templated, reusable deployment | Multiple environments |
| **Production Ready** | Health checks, resources, scaling | Real applications |

---

## Core Workflow

### 1. Clarify Requirements

Ask user about THEIR specific needs:

| Question | Purpose |
|----------|---------|
| **Application type** | Node.js, Python, Go, Java, or other? |
| **Build process** | npm/pip/go build, multi-stage needed? |
| **Port** | Which port does the app listen on? |
| **Environment variables** | What configuration is needed? |
| **Dependencies** | External services (database, cache, APIs)? |
| **Scaling** | Single instance or multiple replicas? |
| **Storage** | Persistent volumes needed? |

### 2. Create Dockerfile

Build optimized container image:

```dockerfile
# Multi-stage build for Node.js
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
USER node
CMD ["node", "server.js"]
```

### 3. Build and Test Docker Image

```bash
# Build image
docker build -t myapp:latest .

# Test locally
docker run -p 3000:3000 myapp:latest

# Tag for registry
docker tag myapp:latest myregistry/myapp:v1.0.0
```

### 4. Create Kubernetes Manifests

Define Deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
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
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

Define Service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP
```

### 5. Create Helm Chart (Optional)

Generate chart structure:

```bash
helm create myapp
```

Customize `values.yaml`:

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi
```

### 6. Deploy to Minikube

Start Minikube and deploy:

```bash
# Start Minikube
minikube start

# Load image into Minikube
minikube image load myapp:latest

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Or use Helm
helm install myapp ./myapp-chart

# Check status
kubectl get pods
kubectl get services

# Access application
minikube service myapp-service
```

### 7. Verify and Test

```bash
# Check pod logs
kubectl logs -l app=myapp

# Port forward for testing
kubectl port-forward service/myapp-service 8080:80

# Test endpoint
curl http://localhost:8080/health

# Check resource usage
kubectl top pods
```

---

## Quick Start Examples

### Simple Node.js App

**Dockerfile:**
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
USER node
CMD ["node", "index.js"]
```

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nodejs-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nodejs-app
  template:
    metadata:
      labels:
        app: nodejs-app
    spec:
      containers:
      - name: nodejs-app
        image: nodejs-app:latest
        ports:
        - containerPort: 3000
---
apiVersion: v1
kind: Service
metadata:
  name: nodejs-app
spec:
  selector:
    app: nodejs-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

**Deploy:**
```bash
docker build -t nodejs-app:latest .
minikube start
minikube image load nodejs-app:latest
kubectl apply -f deployment.yaml
minikube service nodejs-app
```

### Python FastAPI App

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
      - name: fastapi-app
        image: fastapi-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
```

See `references/docker-basics.md` for complete examples.

---

## Key Concepts

### Docker Multi-Stage Builds

Reduce image size by separating build and runtime:

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### Kubernetes Deployments

Manage pod lifecycle and scaling:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3                    # Number of pods
  strategy:
    type: RollingUpdate          # Update strategy
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
        image: myapp:v1.0.0
```

### ConfigMaps and Secrets

Manage configuration:

```yaml
# ConfigMap for non-sensitive data
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  API_URL: "https://api.example.com"
  LOG_LEVEL: "info"

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-password: "supersecret"
  api-key: "abc123"
```

Use in deployment:

```yaml
containers:
- name: myapp
  envFrom:
  - configMapRef:
      name: app-config
  - secretRef:
      name: app-secrets
```

### Health Checks

Ensure pod reliability:

```yaml
livenessProbe:          # Restart if unhealthy
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:         # Remove from service if not ready
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Resource Management

Set CPU and memory limits:

```yaml
resources:
  requests:              # Minimum guaranteed
    memory: "128Mi"
    cpu: "100m"
  limits:                # Maximum allowed
    memory: "256Mi"
    cpu: "200m"
```

### Helm Values

Template configurations:

```yaml
# values.yaml
image:
  repository: myapp
  tag: "1.0.0"

service:
  port: 80

# templates/deployment.yaml
image: {{ .Values.image.repository }}:{{ .Values.image.tag }}
```

---

## Common Patterns

### Pattern: Environment-Specific Configuration

```bash
# Development
helm install myapp ./chart -f values-dev.yaml

# Production
helm install myapp ./chart -f values-prod.yaml
```

### Pattern: Rolling Updates

```bash
# Update image
kubectl set image deployment/myapp myapp=myapp:v2.0.0

# Check rollout status
kubectl rollout status deployment/myapp

# Rollback if needed
kubectl rollout undo deployment/myapp
```

### Pattern: Horizontal Pod Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Pattern: Ingress for External Access

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: myapp.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Pattern: Init Containers

Run setup tasks before main container:

```yaml
initContainers:
- name: init-db
  image: busybox
  command: ['sh', '-c', 'until nc -z db-service 5432; do sleep 1; done']
```

See `references/kubernetes-manifests.md` for complete patterns.

---

## Dependencies

### Required Tools

```bash
# Docker
# Install from https://docs.docker.com/get-docker/

# Kubectl
# Install from https://kubernetes.io/docs/tasks/tools/

# Minikube
# Install from https://minikube.sigs.k8s.io/docs/start/

# Helm (optional)
# Install from https://helm.sh/docs/intro/install/
```

### Verify Installation

```bash
docker --version
kubectl version --client
minikube version
helm version
```

---

## Minikube Setup

### Start Minikube

```bash
# Start with default settings
minikube start

# Start with specific resources
minikube start --cpus=4 --memory=8192

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### Load Images

```bash
# Load local image
minikube image load myapp:latest

# Or use Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t myapp:latest .
```

### Access Services

```bash
# Get service URL
minikube service myapp-service --url

# Open in browser
minikube service myapp-service

# Port forward
kubectl port-forward service/myapp-service 8080:80
```

---

## Production Checklist

Before deploying to production:

- [ ] Use multi-stage Docker builds for smaller images
- [ ] Set resource requests and limits
- [ ] Implement liveness and readiness probes
- [ ] Use ConfigMaps and Secrets for configuration
- [ ] Set up proper logging (stdout/stderr)
- [ ] Configure horizontal pod autoscaling
- [ ] Set up ingress with TLS/SSL
- [ ] Use non-root user in containers
- [ ] Scan images for vulnerabilities
- [ ] Set up monitoring and alerting
- [ ] Configure network policies
- [ ] Implement backup strategies for persistent data
- [ ] Test rollback procedures
- [ ] Document deployment process

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **ImagePullBackOff** | Load image to Minikube: `minikube image load myapp:latest` |
| **CrashLoopBackOff** | Check logs: `kubectl logs <pod-name>` |
| **Pending pods** | Check resources: `kubectl describe pod <pod-name>` |
| **Service not accessible** | Verify service: `kubectl get svc` and `minikube service list` |
| **Port conflicts** | Check Minikube IP: `minikube ip` |
| **Out of memory** | Increase Minikube resources: `minikube start --memory=8192` |

### Debug Commands

```bash
# Check pod status
kubectl get pods -o wide

# View pod logs
kubectl logs <pod-name> -f

# Describe pod for events
kubectl describe pod <pod-name>

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods
kubectl top nodes

# View all resources
kubectl get all

# Check Minikube status
minikube status
minikube logs
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/docker-basics.md` | Dockerfile patterns, multi-stage builds, optimization |
| `references/kubernetes-manifests.md` | Deployments, Services, ConfigMaps, Secrets, Ingress |
| `references/helm-charts.md` | Chart structure, templating, values management |
| `references/minikube-deployment.md` | Local deployment workflows, testing, debugging |

---

## Example: Complete Deployment

**Dockerfile:**
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
USER node
CMD ["node", "dist/server.js"]
```

**kubernetes/deployment.yaml:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@db:5432/mydb"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
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
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
          name: http
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

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer
```

**Deploy:**
```bash
# Build image
docker build -t myapp:latest .

# Start Minikube
minikube start

# Load image
minikube image load myapp:latest

# Apply manifests
kubectl apply -f kubernetes/

# Check status
kubectl get pods
kubectl get services

# Access application
minikube service myapp-service

# View logs
kubectl logs -l app=myapp -f
```

---

## Next Steps

After basic deployment:

1. **Add Helm Chart**: Package for reusability
2. **Set Up Ingress**: Configure external access
3. **Add Monitoring**: Prometheus and Grafana
4. **Implement CI/CD**: Automate builds and deployments
5. **Add Persistent Storage**: For stateful components
6. **Configure Autoscaling**: HPA and VPA
7. **Set Up Logging**: Centralized log aggregation
8. **Security Hardening**: Network policies, RBAC, pod security

See reference files for detailed guidance on each step.
