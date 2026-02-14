# Research: MCP Server Deployment Fix

**Feature**: Fix MCP Server Deployment Issues
**Date**: 2026-02-13
**Status**: Complete

## Overview

Research findings for resolving ImagePullBackOff and ImportError issues in MCP server Kubernetes deployment.

## Research Areas

### 1. Docker Build Context and Python Module Structure

**Problem**: Dockerfile at `app/mcp_server/Dockerfile` copies only `mcp_server/` contents, breaking imports that reference `app.mcp_tools.*`

**Decision**: Create new Dockerfile at backend root with proper build context

**Rationale**:
- Python imports in `server.py` expect `app.mcp_tools.*` structure (lines 10-14)
- Current Dockerfile copies only `mcp_server/` directory, losing parent `app/` structure
- Relative imports in `main.py` (`from .server import server`) fail when run directly
- Standalone entry point exists at `phaseIV/backend/mcp_server_entry.py` with correct absolute imports

**Alternatives Considered**:
1. ❌ **Rewrite all imports to be relative** - Would break integration with backend service
2. ❌ **Copy entire repository** - Unnecessarily large Docker image
3. ✅ **Build from backend root, copy app/ directory** - Maintains structure, minimal size
4. ✅ **Use standalone entry point** - Already exists with correct imports

**Best Practice Reference**:
- Docker multi-stage builds for Python: Use WORKDIR matching Python package structure
- Python packaging: Maintain consistent import paths between development and production
- Container CMD: Use `python -m package.module` for packages with relative imports

### 2. Kubernetes imagePullPolicy Options

**Problem**: Pods attempt to pull `mcp-server:latest` from external registry despite local image existence

**Current State**: Deployment YAML already has `imagePullPolicy: IfNotPresent` (line 21)

**Decision**: Validate existing configuration, ensure image is loaded into Minikube

**Rationale**:
- `IfNotPresent` is correct policy for local development
- Issue occurs when image not present in Minikube's Docker daemon
- Minikube uses separate Docker daemon from host

**Kubernetes imagePullPolicy Options**:
- `Always` - Pull on every pod start (default for :latest tag without explicit policy)
- `IfNotPresent` - Pull only if not cached locally (correct for local development)
- `Never` - Never pull, fail if not present (too strict for this use case)

**Alternatives Considered**:
1. ❌ **Use `Never` policy** - Too restrictive, breaks if image accidentally deleted
2. ✅ **Use `IfNotPresent` policy** - Already configured, correct choice
3. ❌ **Use specific image tag** - Good practice but doesn't solve loading issue

### 3. Minikube Image Loading Strategies

**Problem**: Local Docker image `mcp-server:latest` not available in Minikube's Docker environment

**Decision**: Use `minikube image load` command to transfer image

**Rationale**:
- Minikube runs in isolated VM/container with separate Docker daemon
- Host Docker images not automatically available to Minikube
- Three main strategies exist, each with tradeoffs

**Strategies Compared**:

| Strategy | Command | Pros | Cons | Verdict |
|----------|---------|------|------|---------|
| Direct load | `minikube image load mcp-server:latest` | Simple, explicit | Requires rebuild on changes | ✅ **RECOMMENDED** |
| Docker env | `eval $(minikube docker-env)` | Build directly in Minikube | Pollutes local shell | ✅ **ALTERNATIVE** |
| Registry | Push to registry, pull from Minikube | Production-like | Complex for local dev | ❌ |
| Cache | `minikube cache add` | Automatic reload | Deprecated in newer versions | ❌ |

**Best Practice**: Use `minikube image load` for explicit image management, or `minikube docker-env` for build-test cycles

### 4. Python Module Execution in Docker

**Problem**: Dockerfile CMD `uvicorn main:app` fails because:
- `main.py` uses relative imports (`from .server import server`)
- No `app` variable defined in `main.py`
- MCP server uses custom `.run()` method, not ASGI app

**Decision**: Use `CMD ["python", "mcp_server_entry.py"]` to run standalone entry point

**Rationale**:
- Entry point `mcp_server_entry.py` already exists with correct absolute imports
- Uses `server.run()` method which starts MCP server properly
- Avoids module execution complexity while maintaining correct imports

**Alternatives Considered**:
1. ❌ **`python -m app.mcp_server.main`** - Requires PYTHONPATH setup, more complex
2. ✅ **`python mcp_server_entry.py`** - Simple, uses existing code, absolute imports
3. ❌ **Create FastAPI app wrapper** - Unnecessary complexity, MCP server not ASGI
4. ❌ **Fix relative imports in main.py** - Would need to duplicate entry point logic

**Module Execution Best Practices**:
- Standalone scripts: Use absolute imports or entry point at package root
- Package modules: Use `python -m package.module` with proper PYTHONPATH
- Docker: Prefer simple entry points over complex module execution

### 5. Health Check Endpoints

**Problem**: Deployment YAML references `/health` and `/ready` endpoints (lines 41, 49)

**Decision**: Verify MCP server exposes these endpoints via mcp-use SDK

**Rationale**:
- Health checks critical for Kubernetes pod lifecycle management
- Deployment YAML already configured with appropriate timeouts and thresholds
- Need to confirm mcp-use SDK provides these endpoints automatically

**Research Needed**: Check mcp-use SDK documentation for automatic health endpoint provisioning

**Current Configuration** (from deployment YAML):
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8002
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8002
  initialDelaySeconds: 5
  periodSeconds: 5
```

**Fallback Plan**: If endpoints not automatic, add simple FastAPI routes for health checks

## Key Decisions Summary

| Area | Decision | Impact |
|------|----------|--------|
| **Dockerfile Location** | Create `phaseIV/backend/Dockerfile.mcp` | Fixes build context, enables proper imports |
| **Docker CMD** | Use `CMD ["python", "mcp_server_entry.py"]` | Fixes ImportError, uses existing entry point |
| **Image Loading** | Document `minikube image load` workflow | Fixes ImagePullBackOff by ensuring image availability |
| **imagePullPolicy** | Keep `IfNotPresent` (already correct) | Prevents external registry pulls |
| **Entry Point** | Reuse `mcp_server_entry.py` | Avoids code duplication, maintains absolute imports |
| **Health Checks** | Verify/add health endpoints | Ensures pod lifecycle management works |

## Implementation Impact

**Files to Create**:
- `phaseIV/backend/Dockerfile.mcp` - New Dockerfile with correct build context

**Files to Update**:
- `DEPLOYMENT_GUIDE.md` - Add Minikube image loading steps
- `specs/2-fix-mcp-server-deployment/quickstart.md` - Quick reference

**Files to Validate**:
- `mcp-server-deployment.yaml` - Confirm all settings correct
- `mcp-server-service.yaml` - Confirm service configuration
- `phaseIV/backend/mcp_server_entry.py` - Verify entry point works

**No Changes Needed**:
- Application code (server.py, tools, config)
- Kubernetes Service configuration (already correct)
- Deployment replicas, resources, env vars (already correct)

## Next Steps

Proceed to Phase 1:
1. Create `data-model.md` documenting Kubernetes resource structure
2. Create `contracts/` with MCP tool schemas and health endpoint specs
3. Create `quickstart.md` with complete deployment workflow
