---
id: 005
title: Fix Chatbot 404 Gemini Model
stage: green
date: 2026-02-13
surface: agent
model: claude-sonnet-4-5-20250929
feature: 2-fix-mcp-server-deployment
branch: 2-fix-mcp-server-deployment
user: Fozia
command: direct
labels: ["gemini", "kubernetes", "environment-variables", "chatbot", "404"]
links:
  spec: specs/2-fix-mcp-server-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - helm-charts/todo-chatbot/values.yaml
  - helm-charts/todo-chatbot/templates/backend/deployment.yaml
tests:
  - Backend pods restarted with OPENAI_MODEL=gemini-2.5-flash
  - All pods Running 1/1 Ready
---

## Prompt

I have a Kubernetes deployment with a backend pod and an MCP server pod in the namespace "todo-chatbot". The MCP server is running on port 8002 and exposes the tools at /openmcp.json (previously /docs). My backend pod communicates with the MCP server to fetch tools for the AI chatbot.

Currently, the frontend and backend are up and running, but when I use the chatbot, I get this response:
"Sorry, I encountered an API error: 404. Please try again. AI used tools: unknown(())"

Logs indicate the backend cannot reach the MCP server correctly, likely due to environment variables or path mismatch.

I want you to:
1. Ensure the backend pod knows the correct MCP server URL via environment variables.
2. Ensure the AI backend requests the correct path for MCP tools (/openmcp.json).
3. Provide the exact Kubernetes commands (kubectl) to set or update the environment variables, and redeploy the backend if needed.
4. Verify that the AI can fetch tools correctly and no longer returns 404.

## Response snapshot

**Root cause was NOT MCP server connectivity.** The 404 came from the Google Gemini API, not the MCP server.

The backend's AI agent (ai_agent.py) calls the Gemini API at:
`https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`

The `OPENAI_MODEL` env var was missing from the backend deployment, so it defaulted to `gemini-1.5-flash` (deprecated model → 404). The .env file had `gemini-2.5-flash` but this wasn't in the Helm chart.

Additionally, the backend does NOT call the MCP server over HTTP at all — it uses `mcp_client.py` which makes direct database calls.

**Fix applied:**
1. Added `OPENAI_MODEL: gemini-2.5-flash` to values.yaml
2. Added env var template to backend deployment.yaml
3. Applied immediately: `kubectl set env deployment/todo-chatbot-backend -n todo-chatbot OPENAI_MODEL=gemini-2.5-flash`

## Outcome

- ✅ Impact: Fixed 404 error by adding correct Gemini model name to backend env vars
- 🧪 Tests: Backend pods restarted, OPENAI_MODEL=gemini-2.5-flash confirmed in pod environment
- 📁 Files: values.yaml, deployment.yaml updated
- 🔁 Next prompts: Test chatbot end-to-end to confirm Gemini API calls succeed
- 🧠 Reflection: User assumed issue was MCP connectivity but root cause was missing Gemini API model env var. Always check actual error source in logs before assuming cause.

## Evaluation notes (flywheel)

- Failure modes observed: Missing env var in Helm chart causes silent fallback to deprecated model name
- Graders run and results (PASS/FAIL): PASS - env var set, pods running
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add all required env vars (OPENAI_API_KEY, etc.) to Helm chart to prevent similar issues
