# Deployment Guide

## Deploying Backend to Railway

1. **Sign up for Railway** (if you haven't already):
   - Go to https://railway.app
   - Sign in with your GitHub account

2. **Prepare for Deployment**:
   - Make sure you've committed all changes to your repository
   - The backend is in `phaseII/backend/`

3. **Deploy Backend to Railway**:
   - In your Railway dashboard, click "New Project"
   - Select "GitHub" and choose your `hackhton-II` repository
   - Choose the branch where your backend code is (likely main or 018-fix-dashboard-404)
   - Railway will automatically detect this as a Python project

4. **Configure Environment Variables**:
   After the initial deployment, go to your Railway project settings and add these variables:

   - `JWT_SECRET_KEY`: Generate a secure secret key (at least 32 random characters)
   - `DATABASE_URL`: Railway will automatically provision a PostgreSQL database when you add the Database plugin

5. **Add a Database**:
   - In your Railway project, go to the "Plugins" tab
   - Click "Add Plugin" and select "PostgreSQL"
   - Railway will automatically connect it to your backend

6. **Redeploy**:
   - After adding environment variables and the database, click "Deploy" to redeploy with the new settings

## Deploying Frontend to Vercel

1. **Prepare for Deployment**:
   - The frontend is in `phaseII/frontend/`
   - Make sure your `.env.production` file is properly configured

2. **Deploy to Vercel**:
   - Go to https://vercel.com
   - Sign in with your GitHub account
   - Click "New Project" and import your `hackhton-II` repository
   - Vercel will automatically detect this as a Next.js project

3. **Configure Environment Variables in Vercel**:
   In your Vercel project settings, add:
   - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://your-project-id-production.up.railway.app`)
   - `NEXT_PUBLIC_APP_URL`: Your Vercel frontend URL (e.g., `https://hackhton-ii.vercel.app`)

4. **Deployment Settings**:
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Root Directory: `phaseII/frontend`

## Post-Deployment Steps

1. **Test CORS Connection**:
   - Visit your Vercel frontend URL
   - Try signing up/log in to ensure API calls work
   - Check browser developer tools to confirm no CORS errors

2. **Verify Database Connection**:
   - Create a test user account
   - Verify that data is being stored in your Railway PostgreSQL database

3. **Security Best Practices**:
   - Keep your JWT_SECRET_KEY secure
   - Regularly rotate your secret keys
   - Monitor your application logs for any suspicious activity

## Local Kubernetes Deployment (Phase IV)

Deploy the Todo AI Chatbot to a local Kubernetes cluster using Helm and Minikube.

### Prerequisites
- Minikube
- Helm 3.x
- kubectl

### Quick Start
1. **Start Minikube**:
   ```bash
   minikube start --cpus=4 --memory=4096
   ```

2. **Load/Build Images**:
   ```bash
   .\scripts\load-images.ps1
   ```

3. **Deploy**:
   ```bash
   .\scripts\deploy.ps1
   ```

4. **Access**:
   ```bash
   minikube service todo-chatbot-frontend -n todo-chatbot
   ```

For detailed instructions, see [docs/kubernetes/deployment-guide.md](docs/kubernetes/deployment-guide.md).

### MCP Server Deployment to Minikube

Deploy the MCP server as a standalone microservice in the `todo-chatbot` namespace.

#### Prerequisites

- Minikube installed and running (`minikube start`)
- kubectl configured for Minikube (`kubectl config use-context minikube`)
- Docker installed on host machine

#### Step 1: Build the MCP Server Docker Image

```bash
# Build from the backend directory using Dockerfile.mcp
docker build -f phaseIV/backend/Dockerfile.mcp -t mcp-server:latest phaseIV/backend/
```

**Why Dockerfile.mcp?** The original Dockerfile at `app/mcp_server/Dockerfile` has the wrong build context. `Dockerfile.mcp` builds from the backend root, preserving the `app/` directory structure needed for Python imports.

#### Step 2: Load Image into Minikube

```bash
# Minikube uses a separate Docker daemon - images must be explicitly loaded
minikube image load mcp-server:latest

# Verify the image is available
minikube image ls | grep mcp-server
# Expected: docker.io/library/mcp-server:latest
```

#### Step 3: Create Namespace and Secrets

```bash
# Create namespace
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -

# Create secrets from .env file (contains DATABASE_URL and other config)
kubectl create secret generic mcp-server-secrets -n todo-chatbot \
  --from-env-file=phaseIV/backend/.env \
  --dry-run=client -o yaml | kubectl apply -f -
```

#### Step 4: Deploy MCP Server

```bash
# Apply deployment and service (both in one file)
kubectl apply -f mcp-server-deployment.yaml
```

This creates:
- **Deployment**: 2 replicas of `mcp-server:latest` with `imagePullPolicy: IfNotPresent`
- **Service**: ClusterIP service on port 8002, accessible at `http://mcp-server:8002`

#### Step 5: Verify Deployment

```bash
# Check pods are running (expect 2 pods, 1/1 Ready)
kubectl get pods -n todo-chatbot -l app=mcp-server

# Check service has endpoints
kubectl get endpoints -n todo-chatbot mcp-server

# Check logs for successful startup
kubectl logs -n todo-chatbot deployment/mcp-server --tail=20

# Expected log output:
# ✓ Starting...
# ✓ Ready in XXXms
# Uvicorn running on http://0.0.0.0:8002
```

#### Step 6: Test Connectivity

```bash
# Test from another pod in the namespace
kubectl run test-curl --image=curlimages/curl -n todo-chatbot \
  --rm -it --restart=Never -- \
  curl -s http://mcp-server:8002/openmcp.json

# Expected: JSON with 5 tools listed (add_task, list_tasks, complete_task, delete_task, update_task)
```

#### Rebuilding After Code Changes

```bash
# Rebuild image
docker build -f phaseIV/backend/Dockerfile.mcp -t mcp-server:latest phaseIV/backend/

# Force remove old image from Minikube and reload
minikube ssh -- docker rmi -f mcp-server:latest
minikube image load mcp-server:latest

# Restart deployment to use new image
kubectl rollout restart deployment/mcp-server -n todo-chatbot

# Watch rollout status
kubectl rollout status deployment/mcp-server -n todo-chatbot
```

### MCP Server Troubleshooting

#### ImagePullBackOff

**Symptoms**: Pods show `ImagePullBackOff` or `ErrImagePull`

```bash
# Diagnose
kubectl describe pod -n todo-chatbot <pod-name> | grep -A 5 "Events:"

# Fix: Load image into Minikube
minikube image load mcp-server:latest

# Verify image exists in Minikube
minikube image ls | grep mcp-server

# Restart pods
kubectl rollout restart deployment/mcp-server -n todo-chatbot
```

#### CrashLoopBackOff (ImportError)

**Symptoms**: Pods show `CrashLoopBackOff`, logs show `ImportError: attempted relative import`

```bash
# Diagnose
kubectl logs -n todo-chatbot <pod-name>

# Fix: Ensure image was built with Dockerfile.mcp (not the old Dockerfile)
docker build -f phaseIV/backend/Dockerfile.mcp -t mcp-server:latest phaseIV/backend/

# Verify CMD is correct
docker inspect mcp-server:latest --format "{{json .Config.Cmd}}"
# Expected: ["python","mcp_server_entry.py"]

# Reload and restart
minikube ssh -- docker rmi -f mcp-server:latest
minikube image load mcp-server:latest
kubectl rollout restart deployment/mcp-server -n todo-chatbot
```

#### CrashLoopBackOff (Database URL)

**Symptoms**: Pods crash with `sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL`

```bash
# Fix: Create secrets from .env file
kubectl create secret generic mcp-server-secrets -n todo-chatbot \
  --from-env-file=phaseIV/backend/.env \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods
kubectl rollout restart deployment/mcp-server -n todo-chatbot
```

#### Readiness Probe Failures (0/1 Ready)

**Symptoms**: Pods show `Running` but `0/1` Ready

```bash
# Check probe configuration
kubectl describe pod -n todo-chatbot <pod-name> | grep -A 3 "Readiness:"

# Probes should target /docs on port 8002 (mcp-use SDK doesn't provide /health or /ready)
# If probes target wrong path, update mcp-server-deployment.yaml
```

#### Connection Refused from Backend

**Symptoms**: Backend can't reach `http://mcp-server:8002`

```bash
# Check service endpoints exist
kubectl get endpoints -n todo-chatbot mcp-server
# Should show 2 pod IPs

# Check pods are ready
kubectl get pods -n todo-chatbot -l app=mcp-server
# Should show 1/1 READY

# Test DNS resolution
kubectl run test-dns --image=busybox -n todo-chatbot --rm -it --restart=Never -- nslookup mcp-server
```

#### Verification Commands Quick Reference

```bash
# Status overview
kubectl get all -n todo-chatbot -l app=mcp-server

# Pod logs (follow)
kubectl logs -n todo-chatbot -l app=mcp-server --tail=50 -f

# Port forward for local testing
kubectl port-forward -n todo-chatbot svc/mcp-server 8002:8002
# Then: curl http://localhost:8002/docs

# Resource usage
kubectl top pods -n todo-chatbot -l app=mcp-server
```

## Troubleshooting

### Common Issues:

1. **502 Bad Gateway Error**:
   - This usually indicates the backend server is not responding
   - Check that your Procfile has the correct port: `web: uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Verify your `DATABASE_URL` environment variable is correctly set
   - Check that your `JWT_SECRET_KEY` environment variable is set
   - Ensure the database connection string is valid
   - Check Railway logs for specific error details

2. **CORS Errors Persist**:
   - Verify that your Railway backend allows your Vercel domain in the `allowed_origins` setting
   - Check that environment variables are properly set in Railway

3. **Database Connection Issues**:
   - Ensure your Railway PostgreSQL database is properly attached
   - Verify that the `DATABASE_URL` environment variable is correctly configured
   - Check that your Neon database URL is properly formatted

4. **Authentication Failures**:
   - Make sure your `JWT_SECRET_KEY` is set and kept secure (REQUIRED!)
   - The application will not start if `JWT_SECRET_KEY` is not set
   - Use a strong, random secret key (at least 32 characters)
   - Verify that both frontend and backend use the same base URL format (with/without trailing slashes)

5. **Health Check**:
   - Test your backend health at `/health` endpoint
   - This will show database connectivity status

### Logging:
- Check Railway's logs for backend issues: Navigate to Logs tab in Railway dashboard
- Check Vercel's logs for frontend issues in the Vercel dashboard
- Use browser dev tools to inspect network requests

## Redeployment

After making changes:
1. Commit and push to your GitHub repository
2. Railway and Vercel will automatically deploy the new version
3. Monitor the deployment status in respective dashboards