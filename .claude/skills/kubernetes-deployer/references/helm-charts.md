# Helm Charts

Comprehensive guide to creating and managing Helm charts for Kubernetes applications.

## Table of Contents

- [Helm Fundamentals](#helm-fundamentals)
- [Chart Structure](#chart-structure)
- [Templates and Values](#templates-and-values)
- [Built-in Objects](#built-in-objects)
- [Chart Dependencies](#chart-dependencies)
- [Best Practices](#best-practices)

---

## Helm Fundamentals

### What is Helm?

Helm is a package manager for Kubernetes that:
- Packages Kubernetes manifests into reusable charts
- Manages application releases and versions
- Provides templating for configuration management
- Handles dependencies between applications
- Simplifies rollbacks and upgrades

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Chart** | Package of Kubernetes resources |
| **Release** | Instance of a chart running in cluster |
| **Repository** | Collection of charts |
| **Values** | Configuration parameters |
| **Template** | Kubernetes manifest with placeholders |

### Basic Commands

```bash
# Create new chart
helm create myapp

# Install chart
helm install myapp ./myapp-chart

# Install with custom values
helm install myapp ./myapp-chart -f values-prod.yaml

# Upgrade release
helm upgrade myapp ./myapp-chart

# Rollback release
helm rollback myapp 1

# Uninstall release
helm uninstall myapp

# List releases
helm list

# Get release status
helm status myapp

# View release history
helm history myapp
```

---

## Chart Structure

### Directory Layout

```
myapp/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default configuration values
├── charts/             # Chart dependencies
├── templates/          # Kubernetes manifest templates
│   ├── NOTES.txt      # Post-install notes
│   ├── _helpers.tpl   # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
└── .helmignore        # Files to ignore
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 1.0.0        # Chart version
appVersion: "1.0.0"   # Application version

keywords:
  - myapp
  - web
  - api

home: https://github.com/myorg/myapp
sources:
  - https://github.com/myorg/myapp

maintainers:
  - name: John Doe
    email: john@example.com

dependencies:
  - name: postgresql
    version: "12.1.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

### values.yaml

```yaml
# Default values for myapp
replicaCount: 3

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "1.0.0"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations: {}
podSecurityContext: {}

securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  runAsNonRoot: true
  runAsUser: 1000

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: false
  className: "nginx"
  annotations: {}
  hosts:
    - host: myapp.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

nodeSelector: {}
tolerations: []
affinity: {}

env:
  - name: NODE_ENV
    value: production
  - name: LOG_LEVEL
    value: info

configMap:
  data: {}

secrets:
  data: {}
```

---

## Templates and Values

### Basic Template

**templates/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
      - name: {{ .Chart.Name }}
        securityContext:
          {{- toYaml .Values.securityContext | nindent 12 }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
        imagePullPolicy: {{ .Values.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.service.targetPort }}
          protocol: TCP
        livenessProbe:
          httpGet:
            path: /health
            port: http
        readinessProbe:
          httpGet:
            path: /ready
            port: http
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- with .Values.env }}
        env:
          {{- toYaml . | nindent 12 }}
        {{- end }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

### Helper Templates

**templates/_helpers.tpl:**
```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
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
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "myapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "myapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

### Service Template

**templates/service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http
      protocol: TCP
      name: http
  selector:
    {{- include "myapp.selectorLabels" . | nindent 4 }}
```

### Conditional Ingress

**templates/ingress.yaml:**
```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    {{- range .Values.ingress.hosts }}
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            pathType: {{ .pathType }}
            backend:
              service:
                name: {{ include "myapp.fullname" $ }}
                port:
                  number: {{ $.Values.service.port }}
          {{- end }}
    {{- end }}
{{- end }}
```

### ConfigMap Template

**templates/configmap.yaml:**
```yaml
{{- if .Values.configMap.data }}
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
data:
  {{- toYaml .Values.configMap.data | nindent 2 }}
{{- end }}
```

### HPA Template

**templates/hpa.yaml:**
```yaml
{{- if .Values.autoscaling.enabled }}
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "myapp.fullname" . }}
  minReplicas: {{ .Values.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.autoscaling.maxReplicas }}
  metrics:
    {{- if .Values.autoscaling.targetCPUUtilizationPercentage }}
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetCPUUtilizationPercentage }}
    {{- end }}
    {{- if .Values.autoscaling.targetMemoryUtilizationPercentage }}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: {{ .Values.autoscaling.targetMemoryUtilizationPercentage }}
    {{- end }}
{{- end }}
```

---

## Built-in Objects

### Release Object

```yaml
# Release name
{{ .Release.Name }}

# Release namespace
{{ .Release.Namespace }}

# Is this an upgrade?
{{ .Release.IsUpgrade }}

# Is this an install?
{{ .Release.IsInstall }}

# Release revision number
{{ .Release.Revision }}

# Release service (always "Helm")
{{ .Release.Service }}
```

### Chart Object

```yaml
# Chart name
{{ .Chart.Name }}

# Chart version
{{ .Chart.Version }}

# App version
{{ .Chart.AppVersion }}

# Chart description
{{ .Chart.Description }}
```

### Values Object

```yaml
# Access values
{{ .Values.replicaCount }}
{{ .Values.image.repository }}
{{ .Values.service.port }}

# Nested values
{{ .Values.ingress.enabled }}
{{ .Values.resources.limits.cpu }}
```

### Template Functions

```yaml
# String functions
{{ .Values.name | upper }}
{{ .Values.name | lower }}
{{ .Values.name | title }}
{{ .Values.name | quote }}
{{ .Values.name | trunc 63 }}
{{ .Values.name | trimSuffix "-" }}

# Default values
{{ .Values.name | default "myapp" }}

# Conditionals
{{- if .Values.ingress.enabled }}
enabled
{{- else }}
disabled
{{- end }}

# Loops
{{- range .Values.hosts }}
- {{ . }}
{{- end }}

# YAML formatting
{{- toYaml .Values.resources | nindent 12 }}

# Include templates
{{- include "myapp.labels" . | nindent 4 }}
```

---

## Chart Dependencies

### Define Dependencies

**Chart.yaml:**
```yaml
dependencies:
  - name: postgresql
    version: "12.1.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

### Configure Dependencies

**values.yaml:**
```yaml
postgresql:
  enabled: true
  auth:
    username: myapp
    password: changeme
    database: myapp
  primary:
    persistence:
      enabled: true
      size: 10Gi

redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      enabled: false
```

### Update Dependencies

```bash
# Download dependencies
helm dependency update ./myapp

# List dependencies
helm dependency list ./myapp

# Build dependencies
helm dependency build ./myapp
```

---

## Best Practices

### 1. Use Semantic Versioning

```yaml
# Chart.yaml
version: 1.2.3  # MAJOR.MINOR.PATCH
appVersion: "2.0.1"
```

### 2. Document Values

```yaml
# values.yaml with comments
# -- Number of replicas
replicaCount: 3

# -- Image configuration
image:
  # -- Image repository
  repository: myapp
  # -- Image pull policy
  pullPolicy: IfNotPresent
  # -- Image tag (defaults to chart appVersion)
  tag: ""
```

### 3. Provide Sensible Defaults

```yaml
# Good defaults for most use cases
replicaCount: 2
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 200m
    memory: 256Mi
```

### 4. Use Named Templates

```yaml
# templates/_helpers.tpl
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

# Use in templates
name: {{ include "myapp.name" . }}
```

### 5. Validate Values

**templates/validation.yaml:**
```yaml
{{- if and .Values.ingress.enabled (not .Values.ingress.hosts) }}
{{- fail "ingress.hosts is required when ingress is enabled" }}
{{- end }}

{{- if lt (.Values.replicaCount | int) 1 }}
{{- fail "replicaCount must be at least 1" }}
{{- end }}
```

### 6. Use NOTES.txt

**templates/NOTES.txt:**
```
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To access your application:

{{- if .Values.ingress.enabled }}
  http{{ if .Values.ingress.tls }}s{{ end }}://{{ (index .Values.ingress.hosts 0).host }}
{{- else if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "myapp.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
{{- else if contains "LoadBalancer" .Values.service.type }}
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "myapp.fullname" . }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}
{{- else }}
  kubectl port-forward --namespace {{ .Release.Namespace }} svc/{{ include "myapp.fullname" . }} 8080:{{ .Values.service.port }}
  echo "Visit http://127.0.0.1:8080"
{{- end }}
```

---

## Environment-Specific Values

### Development

**values-dev.yaml:**
```yaml
replicaCount: 1

image:
  tag: "dev"
  pullPolicy: Always

resources:
  requests:
    cpu: 50m
    memory: 64Mi
  limits:
    cpu: 100m
    memory: 128Mi

ingress:
  enabled: true
  hosts:
    - host: myapp-dev.local
      paths:
        - path: /
          pathType: Prefix

postgresql:
  enabled: true
  auth:
    password: devpassword
```

### Production

**values-prod.yaml:**
```yaml
replicaCount: 5

image:
  tag: "1.0.0"
  pullPolicy: IfNotPresent

resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

postgresql:
  enabled: true
  auth:
    existingSecret: postgres-secret
  primary:
    persistence:
      enabled: true
      size: 50Gi
```

### Deploy with Values

```bash
# Development
helm install myapp ./myapp-chart -f values-dev.yaml

# Production
helm install myapp ./myapp-chart -f values-prod.yaml

# Override specific values
helm install myapp ./myapp-chart \
  --set replicaCount=5 \
  --set image.tag=2.0.0
```

---

## Testing Charts

### Lint Chart

```bash
helm lint ./myapp-chart
```

### Dry Run

```bash
helm install myapp ./myapp-chart --dry-run --debug
```

### Template Rendering

```bash
# Render all templates
helm template myapp ./myapp-chart

# Render with values
helm template myapp ./myapp-chart -f values-prod.yaml

# Show specific template
helm template myapp ./myapp-chart -s templates/deployment.yaml
```

### Chart Testing

```bash
# Install chart-testing
brew install chart-testing

# Run tests
ct lint --charts ./myapp-chart
ct install --charts ./myapp-chart
```

---

## Complete Example

Create and deploy a complete Helm chart:

```bash
# Create chart
helm create myapp

# Customize templates and values
# (edit files as shown above)

# Lint chart
helm lint ./myapp

# Test rendering
helm template myapp ./myapp --debug

# Install to Minikube
minikube start
helm install myapp ./myapp

# Check status
helm status myapp
kubectl get all -l app.kubernetes.io/instance=myapp

# Upgrade
helm upgrade myapp ./myapp --set replicaCount=5

# Rollback
helm rollback myapp 1

# Uninstall
helm uninstall myapp
```
