---
id: 010
title: Create FastAPI Background Tasks Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "background-tasks", "celery", "skill-creation", "async-workers", "redis-queue"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-background-tasks.md
tests:
  - none (documentation work)
---

## Prompt

Continue (implicit: continue building FastAPI skills ecosystem)

## Response snapshot

Created comprehensive FastAPI Background Tasks & Async Workers skill documentation (24K) at `.claude/skills/fastapi-background-tasks.md`.

The skill covers:

**1. FastAPI BackgroundTasks (Simple Tasks)**
- Basic BackgroundTasks usage for non-blocking operations
- Multiple background tasks in single endpoint
- Background tasks with dependency injection
- When to use vs when NOT to use BackgroundTasks

**2. Celery Integration (Production Tasks)**
- Celery setup and configuration with Redis
- Task definition with retry logic and error handling
- Using Celery tasks in FastAPI endpoints
- Task status checking and result retrieval
- Celery tasks with database access (creating own sessions)
- Running Celery workers with different configurations

**3. Scheduled Tasks (Celery Beat)**
- Celery Beat configuration with cron schedules
- Scheduled task definitions (daily cleanup, hourly sync, periodic processing)
- Running Celery Beat scheduler

**4. Task Monitoring and Error Handling**
- Task result backend for status checking
- Custom task base class with logging callbacks
- Task error handling with retries and exponential backoff
- Task chaining and workflows (chain, group, chord)

**5. Redis Queue (RQ) Alternative**
- RQ setup as simpler alternative to Celery
- RQ configuration with multiple queues
- RQ task definition (simple functions, no decorators)
- Using RQ in FastAPI endpoints
- Running RQ workers

**Best Practices**:
- Task design (idempotent, atomic, minimal data, timeouts, error handling)
- Error handling (retry logic, max retries, logging, status updates, dead letter queues)
- Performance (task routing, worker concurrency, queue monitoring, prefetching, rate limiting)
- Monitoring (execution time, queue depths, failed tasks, lifecycle events)
- Production considerations (separate workers, graceful shutdown, supervisor/systemd, resource limits, health checks)

**Monitoring with Flower**:
- Flower installation and configuration
- Web-based monitoring for Celery tasks

The skill completes the async processing layer for FastAPI applications, enabling long-running operations, scheduled tasks, and scalable background job processing.

## Outcome

- ✅ Impact: Created production-ready FastAPI background tasks skill with comprehensive patterns for simple BackgroundTasks, Celery integration, scheduled tasks, task monitoring, and RQ alternative
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-background-tasks.md (24K)
- 🔁 Next prompts: User may request additional FastAPI skills (WebSockets, file handling, middleware, caching, rate limiting) or begin implementing a FastAPI application with full async task processing
- 🧠 Reflection: This skill adds critical async processing capabilities to the FastAPI ecosystem. Combined with existing skills (routing, validation, configuration, testing, database, migrations), developers can now build APIs that handle long-running operations efficiently without blocking responses, with proper monitoring and error handling for production environments.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
