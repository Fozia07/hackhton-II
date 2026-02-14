# Helm Chart Design: Todo AI Chatbot

**Feature**: Local Kubernetes Deployment of Todo AI Chatbot
**Date**: 2026-02-09
**Chart Version**: 1.0.0

## Overview

This document provides detailed design specifications for the Helm chart that deploys the Todo AI Chatbot frontend and backend services to Kubernetes.

---

## Chart Metadata

### Chart.yaml

```yaml
apiVersion: v2
name: todo-chatbot
description: Helm chart for Todo AI Chatbot Phase IV deployment
type: application
version: 1.0.0
appVersion: "1.0.0"

keywords:
  - todo
  - chatbot
  - ai
  - phase4

home: https://github.com/your-org/todo-chatbot
sources:
  - https://github.com/your-org/todo-chatbot

maintainers:
  - name: Fozia
    email: fozia@example.com

annotations:
  category: Application
  deployment: local-kubernetes
  phase: IV
```

---

## Values Structure

### values.yaml (Complete)

```yaml
# Global configuration
global:
  environment: dev
  imagePullPolicy: IfNotPresent

# Backend service configuration
backend:
  enabled: true
  replicaCount: 2

  image:
    repository: phase4-backend
    tag: latest
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 80
    targetPort: 8000
    annotations: {}

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi

  env:
    AUTH_SERVICE_URL: "https://fozi07-todo-full-stack-app.hf.space"
    LOG_LEVEL: "info"
    PORT: "8000"

  livenessProbe:
    enabled: true
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3

  readinessProbe:
    enabled: true
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3

  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  podAnnotations: {}
  podLabels: {}

  nodeSelector: {}
  tolerations: []
  affinity: {}

# Frontend service configuration
frontend:
  enabled: true
  replicaCount: 2

  image:
    repository: phase4-frontend
    tag: latest
    pullPolicy: IfNotPresent

  service:
    type: NodePort
    port: 80
    targetPort: 3000
    nodePort: 30080
    annotations: {}

  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 100m
      memory: 128Mi

  env:
    BACKEND_URL: ""  # Will be set to backend service name via template
    PORT: "3000"

  livenessProbe:
    enabled: true
    httpGet:
      path: /health
      port: 3000
    initialDelaySeconds: 30
    periodSeconds: 10
    timeoutSeconds: 5
    failureThreshold: 3

  readinessProbe:
    enabled: true
    httpGet:
      path: /health
      port: 3000
    initialDelaySeconds: 5
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3

  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  podAnnotations: {}
  podLabels: {}

  nodeSelector: {}
  tolerations: []
  affinity: {}

# Common labels applied to all resources
commonLabels:
  app.kubernetes.io/name: todo-chatbot
  app.kubernetes.io/instance: "{{ .Release.Name }}"
  app.kubernetes.io/version: "{{ .Chart.AppVersion }}"
  app.kubernetes.io/managed-by: "{{ .Release.Service }}"
```

### values-dev.yaml (Development Overrides)

```yaml
# Development environment overrides
global:
  environment: dev

backend:
  replicaCount: 1  # Single replica for dev
  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 100m
      memory: 128Mi
  env:
    LOG_LEVEL: "debug"

frontend:
  replicaCount: 1  # Single replica for dev
  resources:
    requests:
      cpu: 25m
      memory: 32Mi
    limits:
      cpu: 50m
      memory: 64Mi
```

---

## Template Design

### _helpers.tpl (Template Functions)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-chatbot.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-chatbot.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-chatbot.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-chatbot.labels" -}}
helm.sh/chart: {{ include "todo-chatbot.chart" . }}
{{ include "todo-chatbot.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-chatbot.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-chatbot.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Backend fullname
*/}}
{{- define "todo-chatbot.backend.fullname" -}}
{{- printf "%s-backend" (include "todo-chatbot.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend labels
*/}}
{{- define "todo-chatbot.backend.labels" -}}
{{ include "todo-chatbot.labels" . }}
app.kubernetes.io/component: backend
tier: api
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-chatbot.backend.selectorLabels" -}}
{{ include "todo-chatbot.selectorLabels" . }}
app.kubernetes.io/component: backend
{{- end }}

{{/*
Frontend fullname
*/}}
{{- define "todo-chatbot.frontend.fullname" -}}
{{- printf "%s-frontend" (include "todo-chatbot.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend labels
*/}}
{{- define "todo-chatbot.frontend.labels" -}}
{{ include "todo-chatbot.labels" . }}
app.kubernetes.io/component: frontend
tier: web
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-chatbot.frontend.selectorLabels" -}}
{{ include "todo-chatbot.selectorLabels" . }}
app.kubernetes.io/component: frontend
{{- end }}
```

### Backend Deployment Template

**File**: `templates/backend/deployment.yaml`

```yaml
{{- if .Values.backend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.backend.fullname" . }}
  labels:
    {{- include "todo-chatbot.backend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  strategy:
    type: {{ .Values.backend.strategy.type }}
    {{- if eq .Values.backend.strategy.type "RollingUpdate" }}
    rollingUpdate:
      maxSurge: {{ .Values.backend.strategy.rollingUpdate.maxSurge }}
      maxUnavailable: {{ .Values.backend.strategy.rollingUpdate.maxUnavailable }}
    {{- end }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.backend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/backend/deployment.yaml") . | sha256sum }}
        {{- with .Values.backend.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "todo-chatbot.backend.selectorLabels" . | nindent 8 }}
        {{- with .Values.backend.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      containers:
      - name: backend
        image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
        imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.backend.service.targetPort }}
          protocol: TCP
        env:
        {{- range $key, $value := .Values.backend.env }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- if .Values.backend.livenessProbe.enabled }}
        livenessProbe:
          httpGet:
            path: {{ .Values.backend.livenessProbe.httpGet.path }}
            port: {{ .Values.backend.livenessProbe.httpGet.port }}
          initialDelaySeconds: {{ .Values.backend.livenessProbe.initialDelaySeconds }}
          periodSeconds: {{ .Values.backend.livenessProbe.periodSeconds }}
          timeoutSeconds: {{ .Values.backend.livenessProbe.timeoutSeconds }}
          failureThreshold: {{ .Values.backend.livenessProbe.failureThreshold }}
        {{- end }}
        {{- if .Values.backend.readinessProbe.enabled }}
        readinessProbe:
          httpGet:
            path: {{ .Values.backend.readinessProbe.httpGet.path }}
            port: {{ .Values.backend.readinessProbe.httpGet.port }}
          initialDelaySeconds: {{ .Values.backend.readinessProbe.initialDelaySeconds }}
          periodSeconds: {{ .Values.backend.readinessProbe.periodSeconds }}
          timeoutSeconds: {{ .Values.backend.readinessProbe.timeoutSeconds }}
          failureThreshold: {{ .Values.backend.readinessProbe.failureThreshold }}
        {{- end }}
        resources:
          {{- toYaml .Values.backend.resources | nindent 10 }}
      {{- with .Values.backend.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.backend.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

### Backend Service Template

**File**: `templates/backend/service.yaml`

```yaml
{{- if .Values.backend.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot.backend.fullname" . }}
  labels:
    {{- include "todo-chatbot.backend.labels" . | nindent 4 }}
  {{- with .Values.backend.service.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  type: {{ .Values.backend.service.type }}
  ports:
  - port: {{ .Values.backend.service.port }}
    targetPort: http
    protocol: TCP
    name: http
  selector:
    {{- include "todo-chatbot.backend.selectorLabels" . | nindent 4 }}
{{- end }}
```

### Frontend Deployment Template

**File**: `templates/frontend/deployment.yaml`

```yaml
{{- if .Values.frontend.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-chatbot.frontend.fullname" . }}
  labels:
    {{- include "todo-chatbot.frontend.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  strategy:
    type: {{ .Values.frontend.strategy.type }}
    {{- if eq .Values.frontend.strategy.type "RollingUpdate" }}
    rollingUpdate:
      maxSurge: {{ .Values.frontend.strategy.rollingUpdate.maxSurge }}
      maxUnavailable: {{ .Values.frontend.strategy.rollingUpdate.maxUnavailable }}
    {{- end }}
  selector:
    matchLabels:
      {{- include "todo-chatbot.frontend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/frontend/deployment.yaml") . | sha256sum }}
        {{- with .Values.frontend.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "todo-chatbot.frontend.selectorLabels" . | nindent 8 }}
        {{- with .Values.frontend.podLabels }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
        imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.frontend.service.targetPort }}
          protocol: TCP
        env:
        - name: BACKEND_URL
          value: "http://{{ include "todo-chatbot.backend.fullname" . }}"
        {{- range $key, $value := .Values.frontend.env }}
        {{- if ne $key "BACKEND_URL" }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- end }}
        {{- if .Values.frontend.livenessProbe.enabled }}
        livenessProbe:
          httpGet:
            path: {{ .Values.frontend.livenessProbe.httpGet.path }}
            port: {{ .Values.frontend.livenessProbe.httpGet.port }}
          initialDelaySeconds: {{ .Values.frontend.livenessProbe.initialDelaySeconds }}
          periodSeconds: {{ .Values.frontend.livenessProbe.periodSeconds }}
          timeoutSeconds: {{ .Values.frontend.livenessProbe.timeoutSeconds }}
          failureThreshold: {{ .Values.frontend.livenessProbe.failureThreshold }}
        {{- end }}
        {{- if .Values.frontend.readinessProbe.enabled }}
        readinessProbe:
          httpGet:
            path: {{ .Values.frontend.readinessProbe.httpGet.path }}
            port: {{ .Values.frontend.readinessProbe.httpGet.port }}
          initialDelaySeconds: {{ .Values.frontend.readinessProbe.initialDelaySeconds }}
          periodSeconds: {{ .Values.frontend.readinessProbe.periodSeconds }}
          timeoutSeconds: {{ .Values.frontend.readinessProbe.timeoutSeconds }}
          failureThreshold: {{ .Values.frontend.readinessProbe.failureThreshold }}
        {{- end }}
        resources:
          {{- toYaml .Values.frontend.resources | nindent 10 }}
      {{- with .Values.frontend.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.frontend.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.frontend.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

### Frontend Service Template

**File**: `templates/frontend/service.yaml`

```yaml
{{- if .Values.frontend.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-chatbot.frontend.fullname" . }}
  labels:
    {{- include "todo-chatbot.frontend.labels" . | nindent 4 }}
  {{- with .Values.frontend.service.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  type: {{ .Values.frontend.service.type }}
  ports:
  - port: {{ .Values.frontend.service.port }}
    targetPort: http
    protocol: TCP
    name: http
    {{- if and (eq .Values.frontend.service.type "NodePort") .Values.frontend.service.nodePort }}
    nodePort: {{ .Values.frontend.service.nodePort }}
    {{- end }}
  selector:
    {{- include "todo-chatbot.frontend.selectorLabels" . | nindent 4 }}
{{- end }}
```

### NOTES.txt Template

**File**: `templates/NOTES.txt`

```text
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}

===========================================
Todo AI Chatbot Deployment Status
===========================================

1. Check pod status:
   kubectl get pods -n {{ .Release.Namespace }} -l app.kubernetes.io/instance={{ .Release.Name }}

2. Wait for pods to be ready:
   kubectl wait --for=condition=ready pod -n {{ .Release.Namespace }} -l app.kubernetes.io/instance={{ .Release.Name }} --timeout=120s

3. Access the frontend:
{{- if eq .Values.frontend.service.type "NodePort" }}
   minikube service {{ include "todo-chatbot.frontend.fullname" . }} -n {{ .Release.Namespace }}

   Or get the URL:
   export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "todo-chatbot.frontend.fullname" . }})
   export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
   echo "Frontend URL: http://$NODE_IP:$NODE_PORT"
{{- else if eq .Values.frontend.service.type "LoadBalancer" }}
   export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "todo-chatbot.frontend.fullname" . }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
   echo "Frontend URL: http://$SERVICE_IP:{{ .Values.frontend.service.port }}"
{{- end }}

4. Check backend health:
   kubectl port-forward -n {{ .Release.Namespace }} svc/{{ include "todo-chatbot.backend.fullname" . }} 8000:80
   curl http://localhost:8000/health

5. View logs:
   # Backend logs
   kubectl logs -n {{ .Release.Namespace }} -l app.kubernetes.io/component=backend -f

   # Frontend logs
   kubectl logs -n {{ .Release.Namespace }} -l app.kubernetes.io/component=frontend -f

===========================================
Configuration
===========================================

Backend replicas: {{ .Values.backend.replicaCount }}
Frontend replicas: {{ .Values.frontend.replicaCount }}
Environment: {{ .Values.global.environment }}

Phase II Auth Service: {{ .Values.backend.env.AUTH_SERVICE_URL }}

===========================================
Troubleshooting
===========================================

If pods are not starting:
  kubectl describe pod -n {{ .Release.Namespace }} <pod-name>

If images are not found:
  eval $(minikube docker-env)
  docker images | grep phase4

For more help, see the documentation at:
  specs/1-k8s-todo-deployment/quickstart.md
```

---

## Chart Directory Structure

```
helm-charts/todo-chatbot/
├── Chart.yaml                 # Chart metadata
├── values.yaml                # Default configuration
├── values-dev.yaml            # Development overrides
├── .helmignore                # Files to exclude
├── templates/
│   ├── _helpers.tpl           # Template helper functions
│   ├── NOTES.txt              # Post-install instructions
│   ├── backend/
│   │   ├── deployment.yaml    # Backend Deployment
│   │   └── service.yaml       # Backend Service
│   └── frontend/
│       ├── deployment.yaml    # Frontend Deployment
│       └── service.yaml       # Frontend Service
└── README.md                  # Chart documentation
```

---

## Deployment Commands

### Install
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --create-namespace \
  --namespace todo-chatbot
```

### Install with custom values
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --create-namespace \
  --namespace todo-chatbot \
  --values values-dev.yaml
```

### Upgrade
```bash
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --namespace todo-chatbot
```

### Rollback
```bash
helm rollback todo-chatbot 1 --namespace todo-chatbot
```

### Uninstall
```bash
helm uninstall todo-chatbot --namespace todo-chatbot
```

### Dry-run
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --dry-run --debug \
  --namespace todo-chatbot
```

### Lint
```bash
helm lint ./helm-charts/todo-chatbot
```

---

## Configuration Customization

### Override replica counts
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=3
```

### Override resource limits
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.resources.limits.memory=512Mi \
  --set backend.resources.limits.cpu=500m
```

### Disable a service
```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set frontend.enabled=false
```

---

## Design Principles

1. **Separation of Concerns**: Backend and frontend in separate template directories
2. **Configurability**: All settings exposed via values.yaml
3. **Production-Ready**: Health checks, resource limits, rolling updates
4. **Kubernetes Best Practices**: Proper labels, annotations, selectors
5. **Helm Best Practices**: Helper templates, NOTES.txt, .helmignore
6. **Security**: Non-root users, resource limits, internal services
7. **Observability**: Proper labels for monitoring and logging
8. **Maintainability**: Clear structure, documented values, reusable templates

---

## Validation Checklist

- [ ] Chart.yaml has correct metadata
- [ ] values.yaml has all required configuration
- [ ] _helpers.tpl has all necessary template functions
- [ ] Deployment templates have proper labels and selectors
- [ ] Service templates match deployment selectors
- [ ] Health probes are configured correctly
- [ ] Resource limits are set appropriately
- [ ] Environment variables are templated
- [ ] NOTES.txt provides useful post-install information
- [ ] Chart passes `helm lint`
- [ ] Dry-run produces valid Kubernetes manifests
- [ ] All templates use helper functions for consistency

---

**Design Status**: ✅ Complete - Ready for implementation
