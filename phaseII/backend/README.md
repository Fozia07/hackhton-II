# Phase II Backend

FastAPI backend for the Phase II authentication system with JWT-based authentication and PostgreSQL database.

## Prerequisites

- Python 3.11+
- PostgreSQL database (or Neon hosted)
- Virtual environment tool (venv or UV)

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install -r requirements-dev.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the backend directory:

```env
# Application Configuration
APP_TITLE=Phase 2 Backend
APP_VERSION=0.1.0
DEBUG=False

# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@host:port/database

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3001,http://localhost:3002,https://hackhton-ii.vercel.app
```

**Generate JWT Secret Key**:
```bash
openssl rand -hex 32
```

### 4. Run the Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at http://localhost:8001

## Authentication Endpoints

- `/auth/signup` - POST endpoint to register a new user
- `/auth/signin` - POST endpoint to authenticate a user and receive JWT token

## Other Endpoints

- `/` - Root endpoint that provides basic API information
- `/health` - Health check endpoint that returns system status
- `/test-db` - Test endpoint to verify database session management

## Database Integration

The backend is integrated with Neon PostgreSQL using SQLModel ORM. Key features include:

- User model for authentication data
- FastAPI dependency injection for database sessions
- Automatic table creation on application startup
- Connection pooling and proper resource management

## Authentication System

The backend includes a complete JWT-based authentication system:

- Secure user registration with password hashing (bcrypt)
- User authentication with JWT token generation
- Token validation for protected endpoints
- Environment-driven configuration for security settings

## Project Structure

```
phaseII/
└── backend/
    ├── app/
    │   ├── main.py
    │   ├── core/
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   └── security.py
    │   ├── models/
    │   │   └── user.py
    │   ├── routes/
    │   │   └── auth.py
    │   ├── schemas/
    │   └── deps/
    ├── requirements.txt
    ├── .env.example
    └── README.md
```

## Environment Variables

Copy `.env.example` to `.env` and configure the variables as needed, especially:
- `DATABASE_URL` for database connection
- `JWT_SECRET_KEY` for JWT token signing
- `JWT_ALGORITHM` for JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` for token expiration (default: 30)

## Dependencies

Dependencies are managed using UV and listed in `requirements.txt`.