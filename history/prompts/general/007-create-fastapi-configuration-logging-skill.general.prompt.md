---
id: 007
title: Create FastAPI Configuration Logging Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "configuration", "logging", "skill-creation", "pydantic-settings", "structured-logging"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-config-logging.md
tests:
  - none (documentation work)
---

## Prompt

now build a skill for FastAPI Configuration & Logging Skill.

Your responsibility is to manage application configuration
and logging in a production-safe way.

YOU HANDLE:
- Environment variables (.env)
- Pydantic BaseSettings
- App configuration injection
- Structured logging
- Startup/shutdown logs

## Response snapshot

Created comprehensive FastAPI Configuration & Logging skill documentation (23K) at `.claude/skills/fastapi-config-logging.md`.

The skill covers:

**1. Environment Variables and .env Files**
- Basic .env file structure with all common configuration
- Development .env.example template for version control
- Environment-specific configuration patterns
- Secrets management best practices

**2. Pydantic BaseSettings Configuration**
- Basic Settings class with field validation
- Advanced nested configuration with DatabaseSettings, RedisSettings, LoggingSettings
- Field validators for log_level, environment, database_url
- Properties for environment detection (is_production, is_development)
- Settings loading with error handling
- Nested environment variable support (DB__URL pattern)

**3. Configuration Dependency Injection**
- Cached settings dependency with @lru_cache()
- Settings injection in endpoints
- Configuration-based database engine creation
- Database session dependency with settings

**4. Structured Logging**
- Basic logging setup with configurable levels
- JSONFormatter for structured JSON logging
- Request ID tracking with middleware and context variables
- RequestIDMiddleware for correlation ID propagation
- RequestIDFilter for adding request IDs to log records
- Logging utility functions:
  - log_request() for HTTP request logging
  - log_database_query() for DB performance tracking
  - log_external_api_call() for external service monitoring

**5. Startup and Shutdown Logging**
- Application lifespan with comprehensive logging
- Startup validation logging with error/warning detection
- Database connection testing
- Redis initialization logging
- Configuration validation at startup
- Graceful shutdown with resource cleanup logging

**Complete Integration Example**:
- main.py with full configuration and logging setup
- core/config.py with Settings class
- core/logging.py with JSONFormatter and utilities
- Environment-based logging (JSON for production, text for development)
- Request ID middleware integration
- CORS configuration from settings

**Best Practices**:
- Configuration management (never commit .env, use validators, cache settings)
- Secrets management (minimum 32 chars, use secret managers, never log secrets)
- Logging best practices (structured JSON, request IDs, appropriate levels, no PII)
- Log levels guidance (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Production considerations (log aggregation, rotation, monitoring)

**Testing Patterns**:
- Configuration validation testing
- Environment detection testing
- JSON formatter testing

The skill integrates seamlessly with fastapi-core-routing.md, fastapi-validation-security.md, and sqlmodel.md skills, providing the configuration and observability layer for production FastAPI applications.

## Outcome

- ✅ Impact: Created production-ready FastAPI configuration and logging skill with comprehensive examples for environment management, Pydantic settings, structured logging, and observability
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-config-logging.md (23K)
- 🔁 Next prompts: User may request additional FastAPI skills (testing, background tasks, WebSockets, database migrations) or begin implementing a FastAPI application using the complete skill stack
- 🧠 Reflection: This skill completes the core infrastructure layer for FastAPI applications. Combined with fastapi-core-routing.md (app structure), fastapi-validation-security.md (validation/security), and sqlmodel.md (database), developers now have a complete foundation for building production-ready FastAPI applications with proper configuration management, structured logging, and observability.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
