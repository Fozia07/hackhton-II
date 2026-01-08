# API Contract: Authentication Endpoints

**Feature**: 001-todo-frontend | **Date**: 2026-01-07 | **Version**: 1.0

## Purpose

Define the authentication API contract between the Next.js frontend and FastAPI backend. This contract ensures both teams can develop independently while maintaining compatibility.

## Base URL

```
Production: https://api.example.com
Development: http://localhost:8000
```

## Authentication Flow

```
1. User submits signup/login form
   ↓
2. Frontend calls POST /api/auth/signup or POST /api/auth/login
   ↓
3. Backend validates credentials and creates session
   ↓
4. Backend returns user data (no JWT in response)
   ↓
5. Frontend stores session via Better Auth
   ↓
6. For API calls, frontend requests JWT via GET /api/auth/get-jwt
   ↓
7. Frontend attaches JWT to all subsequent API requests
```

## Endpoints

### POST /api/auth/signup

Create a new user account.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

**Request Headers**:
```
Content-Type: application/json
```

**Validation Rules**:
- `email`: Required, valid email format (RFC 5322)
- `password`: Required, minimum 8 characters, at least one uppercase, one lowercase, one number
- `name`: Required, minimum 2 characters, maximum 100 characters

**Success Response** (201 Created):
```json
{
  "data": {
    "id": "usr_1234567890",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-07T12:00:00Z"
  },
  "message": "Account created successfully"
}
```

**Error Responses**:

400 Bad Request - Validation Error:
```json
{
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": ["Invalid email format"],
    "password": ["Password must contain at least one uppercase letter"]
  }
}
```

409 Conflict - Email Already Exists:
```json
{
  "message": "Email already registered",
  "code": "EMAIL_EXISTS"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### POST /api/auth/login

Authenticate an existing user.

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Request Headers**:
```
Content-Type: application/json
```

**Validation Rules**:
- `email`: Required, valid email format
- `password`: Required

**Success Response** (200 OK):
```json
{
  "data": {
    "id": "usr_1234567890",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-07T12:00:00Z"
  },
  "message": "Login successful"
}
```

**Error Responses**:

401 Unauthorized - Invalid Credentials:
```json
{
  "message": "Invalid email or password",
  "code": "INVALID_CREDENTIALS"
}
```

400 Bad Request - Validation Error:
```json
{
  "message": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": ["Email is required"]
  }
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### POST /api/auth/logout

Log out the current user.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Logout successful"
}
```

**Error Responses**:

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### GET /api/auth/get-jwt

Get a JWT token for the current session (Better Auth integration).

**Note**: This endpoint is called by the frontend to obtain a JWT token for API requests. It validates the Better Auth session and returns a JWT token.

**Request Headers**:
```
Cookie: better-auth-session=<session_id>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-01-07T13:00:00Z"
}
```

**Token Payload**:
```json
{
  "sub": "usr_1234567890",
  "email": "user@example.com",
  "name": "John Doe",
  "iat": 1704628800,
  "exp": 1704632400
}
```

**Error Responses**:

401 Unauthorized - No Session:
```json
{
  "message": "No active session",
  "code": "NO_SESSION"
}
```

401 Unauthorized - Session Expired:
```json
{
  "message": "Session expired",
  "code": "SESSION_EXPIRED"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

---

### GET /api/auth/me

Get the current authenticated user's information.

**Request Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "data": {
    "id": "usr_1234567890",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2026-01-07T12:00:00Z"
  }
}
```

**Error Responses**:

401 Unauthorized - Invalid Token:
```json
{
  "message": "Invalid or expired token",
  "code": "INVALID_TOKEN"
}
```

500 Internal Server Error:
```json
{
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR"
}
```

## Security Requirements

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- No maximum length (backend should hash securely)

### JWT Token Requirements

- Algorithm: HS256 (HMAC with SHA-256)
- Expiration: 1 hour (3600 seconds)
- Issuer: Backend API domain
- Subject: User ID
- Claims: `sub` (user ID), `email`, `name`, `iat` (issued at), `exp` (expiration)

### Session Requirements

- Better Auth session stored in httpOnly cookie
- Session duration: 7 days
- Session refresh: Automatic on activity
- Session invalidation: On logout or password change

## Error Code Reference

| Code | HTTP Status | Description |
|------|-------------|-------------|
| VALIDATION_ERROR | 400 | Request validation failed |
| INVALID_CREDENTIALS | 401 | Email or password incorrect |
| INVALID_TOKEN | 401 | JWT token invalid or expired |
| NO_SESSION | 401 | No Better Auth session found |
| SESSION_EXPIRED | 401 | Better Auth session expired |
| EMAIL_EXISTS | 409 | Email already registered |
| INTERNAL_ERROR | 500 | Unexpected server error |

## Rate Limiting

- Signup: 5 requests per hour per IP
- Login: 10 requests per 15 minutes per IP
- Logout: 20 requests per minute per user
- Get JWT: 60 requests per minute per user
- Get Me: 60 requests per minute per user

## CORS Configuration

**Allowed Origins**:
- Production: `https://app.example.com`
- Development: `http://localhost:3000`

**Allowed Methods**: GET, POST, OPTIONS

**Allowed Headers**: Content-Type, Authorization

**Credentials**: true (for cookies)

## Testing Scenarios

### Happy Path

1. User signs up with valid credentials → 201 Created
2. User logs in with correct credentials → 200 OK
3. Frontend requests JWT token → 200 OK with token
4. Frontend makes API call with JWT → 200 OK
5. User logs out → 200 OK

### Error Scenarios

1. User signs up with existing email → 409 Conflict
2. User logs in with wrong password → 401 Unauthorized
3. Frontend requests JWT without session → 401 Unauthorized
4. Frontend makes API call with expired JWT → 401 Unauthorized
5. User submits invalid email format → 400 Bad Request

## Frontend Implementation Notes

### Better Auth Configuration

```typescript
// lib/auth/client.ts
import { createAuthClient } from "better-auth/react"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  endpoints: {
    signUp: "/api/auth/signup",
    signIn: "/api/auth/login",
    signOut: "/api/auth/logout",
  },
})
```

### JWT Token Retrieval

```typescript
// lib/api/client.ts
async function getJWTToken(): Promise<string> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/get-jwt`, {
    credentials: "include", // Send Better Auth session cookie
  })

  if (!response.ok) {
    throw new Error("Failed to get JWT token")
  }

  const data = await response.json()
  return data.token
}
```

### API Client with JWT

```typescript
// lib/api/client.ts
export const api = {
  async get<T>(endpoint: string): Promise<T> {
    const token = await getJWTToken()
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    })

    if (response.status === 401) {
      // Redirect to login
      window.location.href = "/login"
      throw new Error("Unauthorized")
    }

    return response.json()
  },
  // ... post, put, patch, delete methods
}
```

## Backend Implementation Notes

### JWT Token Generation

```python
# backend/src/auth/jwt.py
import jwt
from datetime import datetime, timedelta

def generate_jwt_token(user_id: str, email: str, name: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "name": name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### JWT Token Validation

```python
# backend/src/auth/jwt.py
def validate_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-07 | Initial contract definition |

## Approval

- Frontend Team: Pending
- Backend Team: Pending
- Security Review: Pending
