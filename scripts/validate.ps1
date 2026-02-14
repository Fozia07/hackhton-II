# Validate Todo AI Chatbot deployment
$Namespace = "todo-chatbot"

Write-Host "Checking pod status..."
kubectl get pods -n $Namespace

Write-Host "Verifying backend health..."
# We use a temporary port-forward for validation
$pf = Start-Process kubectl -ArgumentList "port-forward service/todo-chatbot-backend 8000:80 -n $Namespace" -PassThru -NoNewWindow
Start-Sleep -Seconds 5
try {
    $response = curl.exe -s http://localhost:8000/health
    Write-Host "Backend Health Response: $response"
} finally {
    Stop-Process $pf
}

Write-Host "Verifying frontend accessibility..."
$pf_fe = Start-Process kubectl -ArgumentList "port-forward service/todo-chatbot-frontend 3000:80 -n $Namespace" -PassThru -NoNewWindow
Start-Sleep -Seconds 5
try {
    $fe_response = curl.exe -s -I http://localhost:3000
    Write-Host "Frontend Status: $($fe_response[0])"
} finally {
    Stop-Process $pf_fe
}

Write-Host "Validation complete."
