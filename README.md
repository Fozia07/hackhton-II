# MCP Server Deployment for Todo AI Chatbot

This solution addresses the 500 errors occurring in the Todo AI Chatbot UI by deploying the missing MCP (Model Context Protocol) server to your Kubernetes cluster.

## Problem
- Backend is running fine and returning 200 responses internally
- Chatbot UI shows 500 errors
- Backend cannot reach its MCP server (MCP_SERVER_URL: http://mcp-server:8002)
- MCP service is not deployed in the cluster

## Solution
Deploy MCP server with Kubernetes Deployment and Service that:
- Uses Docker image: `my-org/mcp-server:latest`
- Exposes port 8002 internally
- Can be reached by backend pod at `http://mcp-server:8002`
- Is scalable with 2 replicas
- Has resource requests: cpu=100m, memory=128Mi; limits: cpu=200m, memory=256Mi
- Includes liveness and readiness probes

## Files Created

### mcp-server-deployment.yaml
Contains the Deployment configuration for the MCP server with:
- 2 replicas for high availability
- Resource requests and limits
- Environment variables
- Liveness and readiness probes

### mcp-server-service.yaml
Contains the Service configuration that exposes the MCP server internally within the cluster at `http://mcp-server:8002`

### deploy-mcp-server.sh
Script with commands to deploy and verify the MCP server in your Minikube cluster

## Deployment Steps

1. Ensure your Minikube cluster is running:
   ```bash
   minikube start
   ```

2. Create the namespace and deploy the MCP server:
   ```bash
   kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -
   kubectl apply -f mcp-server-deployment.yaml
   ```

3. Verify the deployment:
   ```bash
   kubectl get deployments -n todo-chatbot
   kubectl get pods -n todo-chatbot
   kubectl get services -n todo-chatbot
   kubectl rollout status deployment/mcp-server -n todo-chatbot
   ```

4. Check the logs to ensure the MCP server is running properly:
   ```bash
   kubectl logs -l app=mcp-server -n todo-chatbot
   ```

## Expected Result
After deploying the MCP server, the backend should be able to connect to it at `http://mcp-server:8002`, and the 500 errors in the chatbot UI should be resolved.