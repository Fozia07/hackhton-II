# Commands to deploy MCP server to your Minikube cluster

# 1. First, ensure your Minikube cluster is running
minikube start

# 2. Create the todo-chatbot namespace if it doesn't exist
kubectl create namespace todo-chatbot --dry-run=client -o yaml | kubectl apply -f -

# 3. Apply the MCP server deployment and service
kubectl apply -f mcp-server-deployment.yaml

# 4. Verify the deployment
kubectl get deployments -n todo-chatbot
kubectl get pods -n todo-chatbot
kubectl get services -n todo-chatbot

# 5. Check the status of the MCP server pods
kubectl rollout status deployment/mcp-server -n todo-chatbot

# 6. View logs from the MCP server pods
kubectl logs -l app=mcp-server -n todo-chatbot

# 7. Port forward to test the service locally (optional)
kubectl port-forward svc/mcp-server -n todo-chatbot 8002:8002

# 8. Verify the service connectivity from inside the cluster
kubectl run test-pod -it --rm --image=curlimages/curl:latest -n todo-chatbot --restart=Never -- \
  curl -v http://mcp-server:8002/health