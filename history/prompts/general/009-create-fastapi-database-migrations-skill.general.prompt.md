---
id: 009
title: Create FastAPI Database Migrations Skill
stage: general
date: 2026-01-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Fozia
command: skill creation
labels: ["fastapi", "database", "migrations", "skill-creation", "alembic", "sqlmodel"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/fastapi-database-migrations.md
tests:
  - none (documentation work)
---

## Prompt

Continue (implicit: continue building FastAPI skills ecosystem)

## Response snapshot

Created comprehensive FastAPI Database Migrations skill documentation (28K) at `.claude/skills/fastapi-database-migrations.md`.

The skill covers:

**1. Alembic Installation and Setup**
- Installation commands for Alembic and database drivers
- Initialization process creating alembic/ directory structure
- Project structure overview

**2. Alembic Configuration**
- alembic.ini configuration with logging and file templates
- env.py configuration for SQLModel integration (sync and async versions)
- Model imports and metadata setup
- Database URL configuration from settings

**3. Creating Migrations**
- Auto-generate migrations from model changes
- Manual migration creation
- Example migrations:
  - Creating tables with indexes
  - Adding columns with default values
  - Modifying column types
  - Adding foreign keys
  - Creating enum types
  - Adding composite indexes

**4. Applying and Rolling Back Migrations**
- Upgrade commands (head, +N, specific revision, --sql)
- Downgrade commands (-N, specific revision, base, --sql)
- Checking current version and history
- Migration status inspection

**5. Data Migrations**
- Data transformation migrations (splitting name into first_name/last_name)
- Bulk data insertion (populating default categories)
- Safe data migration patterns with rollback support

**6. Advanced Migration Patterns**
- Foreign key constraints with CASCADE
- Enum types for PostgreSQL
- Composite indexes for query optimization
- Complex schema changes

**7. Testing Migrations**
- Migration test fixtures with in-memory SQLite
- Testing upgrade and downgrade paths
- Data integrity testing during migrations
- Verification of schema changes

**8. Production Deployment**
- Pre-deployment checklist script
- Migration status checking
- Deployment script with database backup
- Zero-downtime migration strategies (3-step process for adding non-nullable columns)

**Best Practices**:
- Migration creation (review auto-generated, test first, write both upgrade/downgrade)
- Data safety (backup, test rollback, use transactions, validate data)
- Team collaboration (version control, resolve conflicts, document changes)
- Production considerations (maintenance windows, monitoring, rollback plans, staging tests)
- Performance (separate index migrations, batch operations, avoid peak hours)

**Common Issues and Solutions**:
- Migration conflicts (merge migrations)
- Failed migrations (stamp or rollback and fix)
- Out of sync databases (generate sync migration)

The skill completes the database layer for FastAPI applications, integrating with sqlmodel.md and fastapi-core-routing.md skills.

## Outcome

- ✅ Impact: Created production-ready FastAPI database migrations skill with comprehensive Alembic patterns for schema changes, data migrations, testing, and zero-downtime deployments
- 🧪 Tests: No tests required (documentation work)
- 📁 Files: Created .claude/skills/fastapi-database-migrations.md (28K)
- 🔁 Next prompts: User may request additional FastAPI skills (background tasks, WebSockets, file handling, middleware, API documentation) or begin implementing a FastAPI application with full database migration support
- 🧠 Reflection: This skill completes the database management layer for FastAPI applications. Combined with sqlmodel.md (database operations) and fastapi-testing.md (testing), developers now have complete database lifecycle management including schema versioning, safe migrations, and rollback capabilities for production environments.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (documentation work)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
