# Deployment Guide: Todo AI Chatbot on Kubernetes

This guide describes how to deploy the Phase IV Todo AI Chatbot to a local Kubernetes cluster using Helm and Minikube.

## Prerequisites

- **Minikube**: Local Kubernetes cluster
- **kubectl**: Kubernetes command-line tool
- **Helm**: Package manager for Kubernetes
- **Docker**: For building/managing container images

## Deployment Steps

### 1. Start Minikube
```powershell
minikube start --cpus=4 --memory=4096
```

### 2. Prepare Docker Images
Build the images or load them into Minikube:
```powershell
# Point to minikube docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Build backend
docker build -t phaseiv-backend:latest phaseIV/backend

# Build frontend
docker build -t phaseiv-frontend:latest phaseIV/frontend
```

Alternatively, use the provided script:
```powershell
.\scripts\load-images.ps1
```

### 3. Deploy using Helm
```powershell
.\scripts\deploy.ps1
```

### 4. Access the Application
```powershell
minikube service todo-chatbot-frontend -n todo-chatbot
```

## Configuration

Configuration is managed via `helm-charts/todo-chatbot/values.yaml`. Key variables:

- `backend.env.AUTH_SERVICE_URL`: URL of the Phase II auth service (HuggingFace)
- `backend.env.DATABASE_URL`: Connection string for the database
- `backend.env.GEMINI_API_KEY`: API key for Google Gemini
- `frontend.env.NEXT_PUBLIC_AUTH_SERVICE_URL`: Auth URL for client-side login/signup

## Scaling
To scale the application, update the `replicaCount` in `values.yaml` and run:
```powershell
helm upgrade todo-chatbot helm-charts/todo-chatbot -n todo-chatbot
```
