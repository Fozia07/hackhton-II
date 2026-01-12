# Quickstart Guide: JWT-Based User Authentication

## Overview
This guide provides instructions for setting up and using the JWT-based authentication system in the backend application.

## Prerequisites
- Python 3.9+
- UV package manager
- Existing backend with database integration from previous features
- Neon PostgreSQL database instance

## Setup Instructions

### 1. Install Required Dependencies
Add the following dependencies to your requirements.txt:
```
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
```

Install them using UV:
```bash
cd phaseII/backend
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
uv pip install passlib[bcrypt] python-jose[cryptography]
```

### 2. Configure Environment Variables
Update your `.env` file with JWT configuration:
```
JWT_SECRET_KEY=your-super-secret-key-for-jwt-signing
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Generate a Secret Key
For production use, generate a strong secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Usage

### Register a New User (Signup)
Send a POST request to `/auth/signup` with user details:
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123"
}
```

### Authenticate a User (Signin)
Send a POST request to `/auth/signin` with credentials:
```json
{
  "username": "existinguser",
  "password": "userpassword123"
}
```

On successful authentication, you'll receive a response like:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "existinguser"
}
```

### Using the Access Token
Include the token in the Authorization header for protected endpoints:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Testing
To test the authentication system:
1. Ensure your database is configured and accessible
2. Start the application: `uv run uvicorn app.main:app --reload`
3. Register a new user via POST to `/auth/signup`
4. Authenticate the user via POST to `/auth/signin`
5. Verify you receive a valid JWT token

## Troubleshooting
- If signup fails, verify that username/email is unique
- If signin fails, verify that credentials are correct
- If token validation fails, check JWT configuration in environment variables
- Ensure bcrypt and python-jose are properly installed