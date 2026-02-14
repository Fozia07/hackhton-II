# Architecture: Todo AI Chatbot on Kubernetes

## Overview
The Todo AI Chatbot is deployed as a microservices architecture on a local Kubernetes (Minikube) cluster. It consists of two primary services: a Next.js frontend and a FastAPI backend.

## Component Diagram
```text
[ Browser ] 
     |
     v (NodePort: 30080)
[ Frontend Service ] <----------+
     |                          |
     v (ReplicaSet: 2)          |
[ Frontend Pods ]               |
     |                          |
     v (Internal ClusterIP)     |
[ Backend Service ]             |
     |                          |
     v (ReplicaSet: 2)          |
[ Backend Pods ]                |
     |                          |
     +-----> [ Database ] (External: Neon Postgres)
     |
     +-----> [ Auth Service ] (External: HuggingFace Phase II)
     |
     +-----> [ AI Service ] (External: Google Gemini)
```

## Kubernetes Resources
- **Deployments**: Manage the lifecycle of Frontend and Backend pods.
- **Services**: 
  - `frontend`: NodePort service for external access.
  - `backend`: ClusterIP service for internal communication.
- **ConfigMaps/Env**: Environment variables handle service discovery and external API keys.
- **Probes**: 
  - Liveness: Restarts pods if the application hangs.
  - Readiness: Ensures pods only receive traffic when fully initialized.

## Data Flow
1. User accesses the Frontend via Minikube's NodePort.
2. Frontend interacts with the Phase II Auth Service for login/signup.
3. Once authenticated, Frontend sends requests to the Backend Service.
4. Backend communicates with Neon Postgres for data and Gemini API for AI features.
