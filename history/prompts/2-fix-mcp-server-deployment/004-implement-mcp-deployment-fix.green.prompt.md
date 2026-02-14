---
id: 004
title: Implement MCP Deployment Fix
stage: green
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fix-mcp-server-deployment
branch: 2-fix-mcp-server-deployment
user: Fozia
command: /sp.implement
labels: ["kubernetes", "docker", "deployment", "mcp-server", "minikube", "implementation"]
links:
  spec: specs/2-fix-mcp-server-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phaseIV/backend/Dockerfile.mcp
  - phaseIV/backend/app/mcp_server/Dockerfile
  - mcp-server-deployment.yaml
  - DEPLOYMENT_GUIDE.md
  - specs/2-fix-mcp-server-deployment/tasks.md
tests:
  - 2 pods Running with 1/1 Ready in todo-chatbot namespace
  - Zero ImagePullBackOff errors
  - Zero ImportError/CrashLoopBackOff errors
  - Cross-pod connectivity to http://mcp-server:8002 returns HTTP 200
  - MCP tools confirmed via /openmcp.json (5 tools listed)
  - Service endpoints show 2 pod IPs
  - Health probes passing continuously
---

## Prompt

(No additional input - user invoked /sp.implement command)

## Response snapshot

Executed all 25 tasks across 6 phases. All tasks completed successfully.

**Phase 1: Setup (T001-T004)** - Validated prerequisites:
- Started Minikube (was stopped), kubectl context configured
- Deployment YAML already had correct imagePullPolicy: IfNotPresent, port 8002, 2 replicas, probes
- Service YAML already had correct selector, port 8002, ClusterIP
- Entry point mcp_server_entry.py uses correct absolute imports

**Phase 2: Foundational (T005-T007)** - Created infrastructure:
- Created `phaseIV/backend/Dockerfile.mcp` with correct build context (backend root) and CMD (`python mcp_server_entry.py`)
- Verified requirements.txt includes all dependencies
- Created `todo-chatbot` namespace

**Phase 3: US1 - Pods Running (T008-T012)** - Fixed ImagePullBackOff and ImportError:
- Built Docker image with Dockerfile.mcp
- Loaded image into Minikube (had to force-remove cached old image)
- Discovered missing DATABASE_URL → created Kubernetes Secret from .env file
- Updated deployment YAML to reference secret for DATABASE_URL
- Updated probe paths from /health and /ready to /docs (mcp-use SDK doesn't provide custom health endpoints)
- Result: 2 pods Running, 1/1 Ready, zero errors

**Phase 4: US2 - Connectivity (T013-T018)** - Verified service reachability:
- /docs responds HTTP 200 from within pod
- Service endpoints show 2 pod IPs
- Cross-pod connectivity confirmed (curl from test pod to http://mcp-server:8002/docs returns 200)
- MCP tools confirmed via /openmcp.json (all 5 tools: add_task, list_tasks, complete_task, delete_task, update_task)

**Phase 5: US3 - Documentation (T019-T022)** - Created deployment guide:
- Added comprehensive MCP server deployment section to DEPLOYMENT_GUIDE.md
- Includes: prerequisites, 6-step deployment, rebuild instructions
- Troubleshooting: ImagePullBackOff, CrashLoopBackOff (ImportError), CrashLoopBackOff (Database URL), probe failures, connection refused
- Quick reference verification commands

**Phase 6: Polish (T023-T025)** - Final cleanup:
- Deprecated old Dockerfile with clear deprecation comment
- Validated quickstart.md matches actual deployment
- Full end-to-end validation passed

**Additional fixes discovered during implementation**:
1. DATABASE_URL missing from deployment → added Secret reference
2. Health probe paths /health and /ready return 404 → changed to /docs
3. Old image cached in Minikube → force-removed before reloading

## Outcome

- ✅ Impact: MCP server fully operational in Minikube with 2 Running pods, backend connectivity confirmed, deployment documented
- 🧪 Tests: All 25 tasks completed, all validation checks passed
- 📁 Files: Dockerfile.mcp (created), mcp-server-deployment.yaml (modified), DEPLOYMENT_GUIDE.md (updated), old Dockerfile (deprecated)
- 🔁 Next prompts: `/sp.git.commit_pr` to commit changes and create PR
- 🧠 Reflection: Three additional issues discovered beyond the original spec: missing DATABASE_URL, missing health endpoints, and stale cached image in Minikube. Each was resolved without changing MCP server application code. The mcp-use SDK's `/docs` endpoint serves as an adequate probe target.

## Evaluation notes (flywheel)

- Failure modes observed: (1) Old image cached in Minikube - minikube image load didn't overwrite, needed docker rmi -f first. (2) DATABASE_URL not in deployment YAML - MCP tools import database modules at module load time. (3) mcp-use SDK doesn't provide /health or /ready endpoints - need to use /docs instead.
- Graders run and results (PASS/FAIL): All 25 tasks PASS. End-to-end validation PASS. SC-001 through SC-006 all PASS.
- Prompt variant (if applicable): Standard /sp.implement workflow
- Next experiment (smallest change to try): Consider adding custom /health and /ready endpoints to mcp_server_entry.py for more standard probe behavior. Also consider ConfigMap for non-secret env vars.
