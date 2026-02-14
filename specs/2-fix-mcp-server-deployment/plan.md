# Implementation Plan: Fix MCP Server Deployment Issues

**Branch**: `2-fix-mcp-server-deployment` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/2-fix-mcp-server-deployment/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Fix MCP server deployment in Kubernetes (Minikube) by resolving two critical issues: (1) ImagePullBackOff errors caused by attempting to pull from external registry instead of using local Docker images, and (2) ImportError crashes from incorrect Python module execution. The solution involves correcting the Dockerfile build context and CMD, updating deployment YAML with proper image pull policy, and documenting the complete Minikube deployment workflow.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, uvicorn, mcp-use (MCP Server SDK)
**Storage**: N/A (connects to existing PostgreSQL via backend service)
**Testing**: Manual verification (kubectl, curl), health/readiness probes
**Target Platform**: Kubernetes (Minikube for local, designed for cloud deployment)
**Project Type**: Microservice (containerized MCP server within todo-chatbot namespace)
**Performance Goals**: Handle 100 concurrent tool requests with <1s response time
**Constraints**: <200ms p95 latency, <256Mi memory, must be reachable from backend at http://mcp-server:8002
**Scale/Scope**: 2 replicas, 5 registered tools (add/list/complete/delete/update task)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitution Compliance

✅ **Spec-Driven Development**: Feature has complete specification with requirements and acceptance criteria
✅ **Incremental Evolution**: Fix applies to Phase IV (Kubernetes deployment), maintaining Phase III functionality
✅ **AI-Native Design**: MCP server uses mcp-use SDK, integrates with OpenAI Agents SDK
✅ **Code Quality and Documentation**: Clear documentation required (FR-008, FR-009 from spec)
✅ **Architecture-First Approach**: Microservices architecture maintained, MCP server as independent service
✅ **Container-First Deployment**: Docker containerization with Kubernetes deployment (aligns with Phase IV)

### Gates Status

| Gate | Status | Details |
|------|--------|---------|
| Spec exists | ✅ PASS | Complete spec at specs/2-fix-mcp-server-deployment/spec.md |
| Constitution alignment | ✅ PASS | Aligns with Phase IV Kubernetes deployment requirements |
| No architecture violations | ✅ PASS | Maintains microservices pattern, no new complexity |
| Dependencies documented | ✅ PASS | Python 3.11, mcp-use, FastAPI, Kubernetes/Minikube |
| Testing approach defined | ✅ PASS | Health probes, manual verification via kubectl/curl |

**Result**: ✅ ALL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/2-fix-mcp-server-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0: Dockerfile best practices, K8s image policies
├── data-model.md        # Phase 1: Deployment resources (Pod, Service, ConfigMap)
├── quickstart.md        # Phase 1: Step-by-step Minikube deployment guide
├── contracts/           # Phase 1: Health/readiness endpoints, MCP tool contracts
└── tasks.md             # Phase 2: Implementation tasks (/sp.tasks command)
```

### Source Code (repository root)

```text
phaseIV/backend/
├── app/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── main.py           # Entry point with relative imports
│   │   ├── server.py         # MCPServer instance with 5 tools
│   │   ├── config.py         # Server configuration
│   │   └── Dockerfile        # ⚠️ ISSUE: Wrong location, wrong build context
│   └── mcp_tools/            # Tool implementations (add/list/complete/delete/update)
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
├── mcp_server_entry.py       # ✅ Standalone entry point (correct imports)
├── requirements.txt
└── Dockerfile                # Main backend Dockerfile

# Kubernetes manifests (repository root)
mcp-server-deployment.yaml    # ✅ Has imagePullPolicy: IfNotPresent
mcp-server-service.yaml       # ClusterIP service on port 8002
```

### Files to Modify/Create

**Modified**:
- `phaseIV/backend/app/mcp_server/Dockerfile` → Fix build context and CMD
- `mcp-server-deployment.yaml` → Already correct, validate configuration
- `mcp-server-service.yaml` → Validate service configuration

**Created**:
- `phaseIV/backend/Dockerfile.mcp` → New Dockerfile with correct context
- `DEPLOYMENT_GUIDE.md` → Complete Minikube deployment instructions
- `specs/2-fix-mcp-server-deployment/quickstart.md` → Quick reference guide

**Structure Decision**: This is a microservice deployment fix within an existing web application. The backend service already exists at `phaseIV/backend/` with separate MCP server module at `app/mcp_server/`. The fix addresses Docker build configuration and Kubernetes deployment without changing the application code structure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations identified. This fix maintains existing architecture and reduces deployment complexity by ensuring pods start reliably.
