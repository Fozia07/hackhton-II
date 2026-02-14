# Load Docker images into Minikube
Write-Host "Loading phaseiv-backend:latest into Minikube..."
minikube image load phaseiv-backend:latest

Write-Host "Loading phaseiv-frontend:latest into Minikube..."
minikube image load phaseiv-frontend:latest

Write-Host "Image loading complete."
minikube image ls | Select-String "phaseiv"
