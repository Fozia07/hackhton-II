# Deploy Todo AI Chatbot using Helm
$Namespace = "todo-chatbot"

Write-Host "Creating namespace $Namespace..."
kubectl create namespace $Namespace --dry-run=client -o yaml | kubectl apply -f -

Write-Host "Installing/Upgrading todo-chatbot Helm chart..."
helm upgrade --install todo-chatbot helm-charts/todo-chatbot -n $Namespace --wait --timeout 5m

Write-Host "Deployment complete."
kubectl get all -n $Namespace
