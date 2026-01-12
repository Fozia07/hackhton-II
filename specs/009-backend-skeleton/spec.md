# Backend Skeleton & UV Environment Setup for Hackathon 2 – Phase 2

## Overview

This feature creates a clean FastAPI backend foundation using UV for Python virtual environment management. The goal is to prepare a structure ready for SQLModel, Neon PostgreSQL, and JWT integration while ensuring compatibility with the existing frontend.

## Actors & Roles

- **Backend Developers**: Will use the skeleton to build backend features
- **Hackathon Reviewers**: Evaluate backend readiness and structure
- **DevOps Engineers**: Deploy and maintain the backend infrastructure

## Scope

### In Scope
- Create a dedicated `phase-2/backend` folder with FastAPI foundation
- Initialize UV virtual environment for Python dependency management
- Set up basic FastAPI application with health check endpoint
- Configure project structure following specified layout
- Create documentation for running the backend

### Out of Scope
- Implementing business logic or user features
- Setting up database tables or migrations
- Creating authentication routes or JWT verification
- Frontend modifications
- Production deployment configurations

## Assumptions

- Python 3.9+ is available on development machines
- UV package manager is installed globally
- Frontend application already exists and will integrate with backend
- Neon PostgreSQL will be used as the production database
- Better Auth JWT integration will happen in a subsequent phase

## User Scenarios & Testing

### Scenario 1: Developer Sets Up Backend Environment
- **Given**: Developer has cloned the repository
- **When**: Developer navigates to `phase-2/backend` and runs setup commands
- **Then**: UV virtual environment is created and activated successfully

### Scenario 2: Developer Starts Backend Server
- **Given**: Backend environment is properly set up
- **When**: Developer runs the startup command
- **Then**: FastAPI server starts and is accessible at configured port

### Scenario 3: Health Check Endpoint Verification
- **Given**: Backend server is running
- **When**: Client makes GET request to `/health` endpoint
- **Then**: Server returns `{ "status": "ok" }` response

## Functional Requirements

### FR-1: Backend Directory Structure
- **Requirement**: Create `phase-2/backend` directory with specified subdirectories
- **Acceptance Criteria**:
  - App directory contains main.py entry point
  - Core directory contains config.py, database.py, and security.py
  - Models, schemas, routes, and deps directories exist
  - Requirements file, .env.example, and README.md are present

### FR-2: UV Virtual Environment Setup
- **Requirement**: Initialize UV virtual environment in backend directory
- **Acceptance Criteria**:
  - UV environment can be created and activated
  - Dependencies install correctly using UV
  - Backend can be started using `uv run` commands

### FR-3: FastAPI Application Foundation
- **Requirement**: Create basic FastAPI application with essential configurations
- **Acceptance Criteria**:
  - Application follows FastAPI best practices
  - CORS is configurable via environment variables
  - Server can start without errors

### FR-4: Health Check Endpoint
- **Requirement**: Implement `/health` endpoint that returns system status
- **Acceptance Criteria**:
  - Endpoint returns `{ "status": "ok" }` when healthy
  - Response is JSON formatted
  - Endpoint is accessible without authentication

### FR-5: Dependency Management
- **Requirement**: Include necessary dependencies in requirements.txt
- **Acceptance Criteria**:
  - FastAPI and Uvicorn are included
  - SQLModel is included for future database integration
  - Python-dotenv is included for configuration management
  - Psycopg2-binary is included for PostgreSQL connectivity

## Non-Functional Requirements

### Performance
- Application starts within 10 seconds on standard development hardware
- Health check endpoint responds in under 100ms

### Scalability
- Architecture supports horizontal scaling
- Configuration allows for environment-specific settings

### Maintainability
- Code follows Python best practices (PEP 8)
- Structure enables easy addition of new features
- Clear separation of concerns between modules

## Success Criteria

- [ ] Backend server runs successfully without errors
- [ ] `/health` endpoint returns correct status response
- [ ] UV virtual environment is properly initialized and functional
- [ ] Project structure matches specified directory layout
- [ ] Documentation clearly explains how to run the backend
- [ ] Codebase is clean and ready for next development phase
- [ ] Application can be started using `uv run uvicorn app.main:app --reload`

## Key Entities

### Configuration
- Application settings loaded from environment variables
- Database connection parameters
- CORS configuration options

### Security
- Security scaffolding prepared for JWT integration
- Authentication layer structure established

### Database
- Database connection scaffolding ready for SQLModel integration
- Engine configuration prepared for Neon PostgreSQL

## Constraints

- Language: Python only
- Framework: FastAPI (as specified)
- Environment manager: UV (mandatory)
- Format: Clean project skeleton without business logic
- Scope: Backend foundation only, no frontend modifications