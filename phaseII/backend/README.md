# Backend for Hackathon 2 – Phase 2

This is the backend for the Hackathon 2 project, built with FastAPI and integrated with Neon PostgreSQL database using SQLModel. It's prepared for integration with the existing frontend and includes JWT-based authentication.

## Prerequisites

- Python 3.9+
- UV package manager
- Neon PostgreSQL database instance (for production)

## Setup

1. Navigate to this directory: `cd phaseII/backend`
2. Create and activate the UV virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
4. Configure your database connection by copying `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
5. Update the environment variables in `.env`:
   - `DATABASE_URL` with your Neon PostgreSQL connection string:
     ```
     DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
     ```
   - `JWT_SECRET_KEY` with a strong secret key for JWT signing
   - `JWT_ALGORITHM` (default: HS256)
   - `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30)

## Running the Backend

To start the backend server:

```bash

\
```

The server will start at `http://localhost:8000` by default.

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