---
id: 001
title: Fix MCP Server Deployment Spec
stage: spec
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fix-mcp-server-deployment
branch: 2-fix-mcp-server-deployment
user: Fozia
command: /sp.specify
labels: ["kubernetes", "deployment", "mcp-server", "minikube", "docker"]
links:
  spec: specs/2-fix-mcp-server-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/2-fix-mcp-server-deployment/spec.md
  - specs/2-fix-mcp-server-deployment/checklists/requirements.md
tests:
  - Specification quality checklist validation
---

## Prompt

Hi Claude,

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

Give updated YAML, Docker CMD fix, and instructions.

## Response snapshot

Found existing specification at `specs/2-fix-mcp-server-deployment/spec.md` with identical problem description. Created and checked out branch `2-fix-mcp-server-deployment`.

Validated specification against quality checklist:
- All mandatory sections complete (User Scenarios, Requirements, Success Criteria)
- 9 functional requirements, all testable
- 6 measurable success criteria
- 3 prioritized user stories with clear acceptance scenarios
- Edge cases identified

Minor notes on implementation details: While spec contains Kubernetes/Docker specifics, this is acceptable for infrastructure fixes where these details are part of the problem domain itself.

Created quality checklist at `specs/2-fix-mcp-server-deployment/checklists/requirements.md` with status: **READY FOR PLANNING**

## Outcome

- ✅ Impact: Specification validated and ready for planning phase. Feature #2 reactivated with proper branch.
- 🧪 Tests: Quality checklist validation completed - all mandatory criteria met
- 📁 Files: spec.md (existing, validated), checklists/requirements.md (created)
- 🔁 Next prompts: `/sp.plan` to create architecture plan, or `/sp.clarify` if requirements need refinement
- 🧠 Reflection: Discovered existing feature #2 with identical requirements, avoided duplicate creation. Infrastructure specs appropriately contain technology details as they define the problem domain.

## Evaluation notes (flywheel)

- Failure modes observed: Initial attempt to create new feature would have duplicated existing spec #2. Bash PHR script unavailable on Windows platform.
- Graders run and results (PASS/FAIL): Quality checklist PASS - specification complete and ready
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Consider slight rewording of SC-002 and SC-003 to use more generic error terminology, though current version is acceptable for infrastructure domain
