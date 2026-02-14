# Cleanup Todo AI Chatbot deployment
$Namespace = "todo-chatbot"

Write-Host "Uninstalling Helm release..."
helm uninstall todo-chatbot -n $Namespace

Write-Host "Deleting namespace $Namespace..."
kubectl delete namespace $Namespace

Write-Host "Cleanup complete."
