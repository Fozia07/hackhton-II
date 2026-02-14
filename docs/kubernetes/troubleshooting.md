# Troubleshooting Guide: Todo AI Chatbot on Kubernetes

## Common Issues

### Pods in CrashLoopBackOff

1. **Check Logs**:
   ```bash
   kubectl logs -l component=backend -n todo-chatbot
   ```
2. **Missing Environment Variables**: Ensure `DATABASE_URL` and `GEMINI_API_KEY` are correctly set in `values.yaml`.
3. **Database Connection**: Verify the backend can reach the PostgreSQL database on Neon.

### Probes Failing

1. **Backend**: Check if the application is listening on port 8000 and has a `/health` endpoint.
2. **Frontend**: The frontend uses `/` for health checks. Ensure the Next.js server is fully started.

### Images Not Found

If Kubernetes fails to pull images:
1. Ensure the image name in `values.yaml` matches the one in Minikube.
2. Verify images are in Minikube's registry: `minikube image ls`.
3. Check `imagePullPolicy` is set to `IfNotPresent`.

### Authentication Failures

1. Verify `NEXT_PUBLIC_AUTH_SERVICE_URL` is set to the correct HuggingFace URL.
2. Ensure the `SECRET_KEY` matches between Phase II and Phase IV for JWT verification.

## Debugging Commands

- **Describe Pod**: `kubectl describe pod <pod-name> -n todo-chatbot`
- **Port-forward Backend**: `kubectl port-forward service/todo-chatbot-backend 8000:80 -n todo-chatbot`
- **View Events**: `kubectl get events -n todo-chatbot --sort-by='.lastTimestamp'`
