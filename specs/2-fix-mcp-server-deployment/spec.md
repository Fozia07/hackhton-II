# Feature Specification: Fix MCP Server Deployment Issues

**Feature Branch**: `2-fix-mcp-server-deployment`
**Created**: 2026-02-12
**Status**: Draft
**Input**: User description: "Hi Claude,

I have an MCP server pod in Kubernetes (namespace: todo-chatbot) with these issues:

1. Pods show `ImagePullBackOff` even though local Docker image `mcp-server:latest` exists.
2. Some pods crash with:

   ImportError: attempted relative import with no known parent package

Setup:

- Deployment YAML uses image `my-org/mcp-server:latest`, port 8002.
- Python app inside `/app/`:

  main.py
  server.py
  __init__.py

- main.py has: `from .server import server`
- Deployment YAML does not have `imagePullPolicy`.

Tasks:

1. Update Deployment YAML so:
   - It uses the local image (`imagePullPolicy: IfNotPresent`)
   - Probes, port, and replicas are correct
2. Fix Python import / Docker CMD to avoid relative import crash
3. Give step-by-step to:
   - Load Docker image into Minikube
   - Apply YAML
   - Verify pods are running
4. Ensure MCP server is reachable from `todo-chatbot-backend` at `http://mcp-server:8002`

Give updated YAML, Docker CMD fix, and instructions."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - MCP Server Pods Start Successfully (Priority: P1)

As a DevOps engineer, I need the MCP server pods to start successfully in Minikube so that the backend service can communicate with them without encountering ImagePullBackOff or import errors.

**Why this priority**: This is the core issue blocking the entire MCP server deployment and preventing the Todo AI Chatbot from functioning.

**Independent Test**: After applying the fixes, all MCP server pods should reach Running status without ImagePullBackOff or CrashLoopBackOff errors.

**Acceptance Scenarios**:

1. **Given** a local Docker image `mcp-server:latest` exists, **When** Kubernetes deployment is applied with correct imagePullPolicy, **Then** pods pull the image from local cache without attempting external registry access
2. **Given** Python application has relative imports, **When** Docker container starts with correct module execution, **Then** application runs without ImportError
3. **Given** MCP server pods are running, **When** checking pod status, **Then** all replicas show Running state with 2/2 ready containers

---

### User Story 2 - Backend Service Connects to MCP Server (Priority: P2)

As a backend service, I need to successfully connect to the MCP server at `http://mcp-server:8002` so that I can process chatbot requests without returning 500 errors.

**Why this priority**: Ensures end-to-end connectivity between services after deployment fixes are applied.

**Independent Test**: Backend pods can successfully make HTTP requests to `http://mcp-server:8002` and receive valid responses.

**Acceptance Scenarios**:

1. **Given** MCP server is running in the cluster, **When** backend service makes a request to `http://mcp-server:8002/health`, **Then** request succeeds with 200 status code
2. **Given** MCP server service is properly configured, **When** DNS lookup is performed for `mcp-server`, **Then** service IP is resolved correctly within the namespace

---

### User Story 3 - Deployment Process is Documented and Repeatable (Priority: P3)

As a DevOps engineer, I need clear step-by-step instructions to deploy the MCP server to Minikube so that I can reliably reproduce the deployment process.

**Why this priority**: Enables consistent deployments and troubleshooting for future iterations.

**Independent Test**: Following the documented steps results in a successful MCP server deployment from scratch.

**Acceptance Scenarios**:

1. **Given** step-by-step deployment instructions, **When** following each step in sequence, **Then** MCP server deploys successfully without manual intervention
2. **Given** deployment verification commands, **When** executed after deployment, **Then** all health checks pass and pods are confirmed running

---

### Edge Cases

- What happens when the Docker image is not loaded into Minikube before deployment?
- How does the system handle Python import errors if the module structure changes?
- What occurs if the MCP server port 8002 is already in use by another service?
- How does Kubernetes handle pod restarts when liveness probes fail?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use local Docker image `mcp-server:latest` without attempting to pull from external registry
- **FR-002**: System MUST configure imagePullPolicy to prevent ImagePullBackOff errors
- **FR-003**: System MUST execute Python application as a module to avoid relative import errors
- **FR-004**: System MUST expose MCP server on port 8002 within the cluster
- **FR-005**: System MUST allow backend services to reach MCP server at `http://mcp-server:8002`
- **FR-006**: System MUST maintain 2 replicas of the MCP server for high availability
- **FR-007**: System MUST include health check probes to monitor pod status
- **FR-008**: System MUST provide clear deployment instructions for loading images into Minikube
- **FR-009**: System MUST provide verification steps to confirm successful deployment

### Key Entities

- **MCP Server Pod**: Container running the Python MCP server application with proper module execution
- **Docker Image**: Local image `mcp-server:latest` containing the Python application and dependencies
- **Kubernetes Service**: ClusterIP service exposing MCP server at `http://mcp-server:8002`
- **Backend Service**: Consumer of the MCP server that requires reliable connectivity

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: MCP server pods reach Running status within 60 seconds of deployment (100% success rate)
- **SC-002**: Zero ImagePullBackOff errors occur when deploying with local images
- **SC-003**: Zero ImportError crashes occur when MCP server pods start
- **SC-004**: Backend services successfully connect to MCP server with 99% success rate
- **SC-005**: All health check probes pass within 30 seconds of pod startup
- **SC-006**: Deployment process completes successfully following documented steps without manual intervention