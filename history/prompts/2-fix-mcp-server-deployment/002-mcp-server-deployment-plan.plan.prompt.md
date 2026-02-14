---
id: 002
title: MCP Server Deployment Plan
stage: plan
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fix-mcp-server-deployment
branch: 2-fix-mcp-server-deployment
user: Fozia
command: /sp.plan
labels: ["kubernetes", "docker", "deployment", "mcp-server", "architecture"]
links:
  spec: specs/2-fix-mcp-server-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-fix-mcp-server-deployment/plan.md
  - specs/2-fix-mcp-server-deployment/research.md
  - specs/2-fix-mcp-server-deployment/data-model.md
  - specs/2-fix-mcp-server-deployment/quickstart.md
  - specs/2-fix-mcp-server-deployment/contracts/health-endpoints.md
  - specs/2-fix-mcp-server-deployment/contracts/mcp-tools-schema.md
  - CLAUDE.md (agent context updated)
tests:
  - Constitution compliance check - all gates passed
  - Research phase - Docker build context, imagePullPolicy, Python module execution
  - Design phase - Kubernetes resources, health endpoints, MCP tool contracts
---

## Prompt

(No additional input - user invoked /sp.plan command)

## Response snapshot

Created comprehensive implementation plan for fixing MCP server deployment in Kubernetes.

**Phase 0 - Research (research.md)**:
- Docker build context best practices: Must build from `phaseIV/backend/` to preserve `app/` structure
- Python module execution: Use `CMD ["python", "mcp_server_entry.py"]` to avoid ImportError
- Kubernetes imagePullPolicy: Keep `IfNotPresent` (already correct), ensure image loaded via `minikube image load`
- Minikube image loading: Use `minikube image load mcp-server:latest` or `minikube docker-env`
- Health check endpoints: Need to verify/implement `/health` and `/ready` for probes

**Phase 1 - Design**:
- **data-model.md**: Kubernetes resources structure (Deployment, Service, Pod specs, constraints, validation rules)
- **contracts/health-endpoints.md**: Liveness (`/health`) and readiness (`/ready`) endpoint specifications
- **contracts/mcp-tools-schema.md**: MCP protocol over HTTP, 5 tool schemas (add/list/complete/delete/update task)
- **quickstart.md**: 8-step deployment guide with troubleshooting for ImagePullBackOff and CrashLoopBackOff

**Key Decisions**:
1. Create new `Dockerfile.mcp` at backend root (not at `app/mcp_server/Dockerfile`)
2. Use existing `mcp_server_entry.py` entry point (absolute imports, correct structure)
3. Document `minikube image load` workflow as primary image loading strategy
4. Validate existing deployment YAML (already has correct `imagePullPolicy: IfNotPresent`)
5. Verify health endpoints exist or implement as fallback

**Technical Context**:
- Language: Python 3.11
- Dependencies: FastAPI, uvicorn, mcp-use (MCP Server SDK)
- Platform: Kubernetes (Minikube local), containerized microservice
- Performance: <200ms p95 latency, <256Mi memory per pod
- Scale: 2 replicas, 5 registered tools

**Constitution Check**: ✅ All gates passed
- Spec-driven development ✅
- Incremental evolution (Phase IV) ✅
- AI-native design (MCP server) ✅
- Container-first deployment ✅
- No violations or complexity additions

**Files to Create/Modify**:
- Create: `phaseIV/backend/Dockerfile.mcp`
- Create: `DEPLOYMENT_GUIDE.md`
- Validate: `mcp-server-deployment.yaml`, `mcp-server-service.yaml`
- Validate: `phaseIV/backend/mcp_server_entry.py`

## Outcome

- ✅ Impact: Complete architectural plan with research, design artifacts, and deployment guide. Ready for task generation.
- 🧪 Tests: Constitution compliance validated, all design artifacts created and validated
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, 2 contract files, CLAUDE.md updated
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Root causes identified (Docker build context, Python imports, image loading). Solutions leverage existing code (mcp_server_entry.py) and standard patterns (minikube image load, IfNotPresent policy). No code changes needed to MCP server logic, only build/deployment configuration.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully with comprehensive research and design
- Graders run and results (PASS/FAIL): Constitution check PASS, all mandatory plan sections complete
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) and Phase 1 (design)
- Next experiment (smallest change to try): Verify if mcp-use SDK auto-provisions health endpoints before implementing manual fallback
