# Data Models: Fix Phase II Authentication 503 Error

**Date**: 2026-02-07
**Feature**: 001-fix-phaseii-503
**Phase**: Phase 1 Design
**Status**: Complete

## Overview

This document describes the data models and schemas used in the Phase II authentication system. No changes to existing data models are required for fixing the 503 error - this is purely a configuration issue. This documentation serves as a reference for understanding the authentication data flow.

---

## User Model

### Database Table: `user`

**Purpose**: Stores user account information and authentication credentials.

**Schema**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `username` | String(150) | Unique, Not Null, Min 3 chars | User's login username |
| `email` | String | Unique, Not Null, Valid email format | User's email address |
| `hashed_password` | String | Not Null | Bcrypt-hashed password (never stored in plain text) |
| `created_at` | DateTime | Not Null, Default: UTC now | Account creation timestamp |
| `updated_at` | DateTime | Not Null, Default: UTC now | Last update timestamp |
| `is_active` | Boolean | Not Null, Default: True | Account active status |

**Implementation**: `phaseII/backend/app/models/user.py:13-31`

**Example**:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJfitzGjO",
  "created_at": "2026-02-07T10:30:00Z",
  "updated_at": "2026-02-07T10:30:00Z",
  "is_active": true
}
```

**Security Notes**:
- Passwords are hashed using bcrypt with 12 rounds (secure)
- `hashed_password` is never exposed in API responses
- Email and username are unique to prevent duplicate accounts

---

## Authentication Schemas

### UserCreate Schema

**Purpose**: Request schema for user signup (POST /auth/signup)

**Fields**:

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| `username` | String | Min 3, Max 150 chars, Required | Desired username |
| `email` | String | Valid email format, Required | User's email address |
| `password` | String | Min 8, Max 72 chars, Required | Plain text password (will be hashed) |

**Implementation**: `phaseII/backend/app/models/user.py:33-43`

**Validation Rules**:
- Username: 3-150 characters
- Email: Must match regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- Password: 8-72 characters (bcrypt limitation)

**Example Request**:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

---

### UserRead Schema

**Purpose**: Response schema for user data (excludes sensitive information)

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | User's unique identifier |
| `username` | String | User's username |
| `email` | String | User's email address |
| `created_at` | DateTime | Account creation timestamp (ISO 8601) |
| `updated_at` | DateTime | Last update timestamp (ISO 8601) |
| `is_active` | Boolean | Account active status |

**Implementation**: `phaseII/backend/app/models/user.py:46-51`

**Example Response**:
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2026-02-07T10:30:00Z",
  "updated_at": "2026-02-07T10:30:00Z",
  "is_active": true
}
```

**Security Note**: `hashed_password` is intentionally excluded from this schema.

---

### UserSignIn Schema

**Purpose**: Request schema for user signin (POST /auth/signin)

**Fields**:

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| `username` | String | Required | Username or email (accepts both) |
| `password` | String | Required | Plain text password |

**Implementation**: `phaseII/backend/app/models/user.py:54-57`

**Example Request**:
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Note**: The `username` field accepts either username or email for flexibility.

---

### SignIn Response Schema

**Purpose**: Response schema for successful signin

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | String | JWT access token |
| `token_type` | String | Token type (always "bearer") |
| `user_id` | Integer | User's unique identifier |
| `username` | String | User's username |

**Implementation**: `phaseII/backend/app/routes/auth.py:131-136`

**Example Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "username": "johndoe"
}
```

**JWT Token Payload**:
```json
{
  "sub": "1",
  "user_id": 1,
  "username": "johndoe",
  "exp": 1707311400,
  "iat": 1707309600
}
```

**Token Details**:
- Algorithm: HS256
- Expiration: 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Secret: Stored in `JWT_SECRET_KEY` environment variable

---

## Health Check Schema

### Current Health Check Response

**Purpose**: Basic health status of the application

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Overall status ("ok" or "error") |
| `database` | String | Database status ("connected", "disconnected", "not configured") |
| `timestamp` | String | Current timestamp (ISO 8601) |

**Implementation**: `phaseII/backend/app/main.py:62-86`

**Example Response (Success)**:
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2026-02-07T12:00:00Z"
}
```

**Example Response (Error)**:
```json
{
  "status": "error",
  "error": "Database connection failed",
  "timestamp": "2026-02-07T12:00:00Z"
}
```

---

### Enhanced Health Check Response (Proposed)

**Purpose**: Comprehensive health status with detailed metrics

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `status` | String | Overall status ("ok", "degraded", "error") |
| `timestamp` | String | Current timestamp (ISO 8601) |
| `version` | String | Application version |
| `database` | Object | Database health details |
| `database.status` | String | Connection status ("connected", "disconnected") |
| `database.latency_ms` | Integer | Database query latency in milliseconds |
| `endpoints` | Object | Endpoint availability status |
| `endpoints.auth` | String | Auth endpoints status ("available", "unavailable") |
| `endpoints.todos` | String | Todo endpoints status ("available", "unavailable") |

**Example Response (Healthy)**:
```json
{
  "status": "ok",
  "timestamp": "2026-02-07T12:00:00Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 15
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

**Example Response (Degraded)**:
```json
{
  "status": "degraded",
  "timestamp": "2026-02-07T12:00:00Z",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "latency_ms": 250
  },
  "endpoints": {
    "auth": "available",
    "todos": "available"
  }
}
```

**Status Determination**:
- `ok`: All services operational, database latency < 100ms
- `degraded`: All services operational, database latency 100-500ms
- `error`: One or more services unavailable or database latency > 500ms

---

## Error Response Schemas

### Standard Error Response

**Purpose**: Consistent error format across all endpoints

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `detail` | String or Object | Error message or detailed error information |

**Implementation**: FastAPI's HTTPException default format

**Example (Simple Error)**:
```json
{
  "detail": "Username already registered"
}
```

**Example (Validation Error)**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

---

### HTTP Status Codes

**Authentication Endpoints**:

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 OK | Success | Successful signin |
| 201 Created | Resource created | Successful signup |
| 400 Bad Request | Invalid input | Validation errors, invalid email format |
| 401 Unauthorized | Authentication failed | Invalid credentials, expired token |
| 409 Conflict | Resource conflict | Username or email already exists |
| 500 Internal Server Error | Server error | Unexpected errors, database failures |

**Health Check Endpoint**:

| Status Code | Meaning | When Used |
|-------------|---------|-----------|
| 200 OK | Healthy | All services operational |
| 503 Service Unavailable | Unhealthy | Database unavailable or critical service down |

---

## Data Flow Diagrams

### Signup Flow

```
Client                    Frontend                  Backend                   Database
  |                          |                         |                         |
  |-- Fill signup form ----->|                         |                         |
  |                          |                         |                         |
  |                          |-- POST /auth/signup --->|                         |
  |                          |   (UserCreate)          |                         |
  |                          |                         |                         |
  |                          |                         |-- Validate email ------>|
  |                          |                         |<- Check existing user --|
  |                          |                         |                         |
  |                          |                         |-- Hash password         |
  |                          |                         |                         |
  |                          |                         |-- INSERT user --------->|
  |                          |                         |<- User created ---------|
  |                          |                         |                         |
  |                          |<- 201 Created ----------|                         |
  |                          |   (UserRead)            |                         |
  |                          |                         |                         |
  |<- Redirect to dashboard -|                         |                         |
```

### Signin Flow

```
Client                    Frontend                  Backend                   Database
  |                          |                         |                         |
  |-- Fill signin form ----->|                         |                         |
  |                          |                         |                         |
  |                          |-- POST /auth/signin --->|                         |
  |                          |   (UserSignIn)          |                         |
  |                          |                         |                         |
  |                          |                         |-- SELECT user --------->|
  |                          |                         |<- User data ------------|
  |                          |                         |                         |
  |                          |                         |-- Verify password       |
  |                          |                         |-- Create JWT token      |
  |                          |                         |                         |
  |                          |<- 200 OK ---------------|                         |
  |                          |   (access_token)        |                         |
  |                          |                         |                         |
  |-- Store token in storage |                         |                         |
  |<- Redirect to dashboard -|                         |                         |
```

---

## Security Considerations

### Password Security

1. **Hashing Algorithm**: bcrypt with 12 rounds
   - Industry standard for password hashing
   - Computationally expensive to prevent brute force attacks
   - Automatically includes salt

2. **Password Requirements**:
   - Minimum 8 characters
   - Maximum 72 characters (bcrypt limitation)
   - No complexity requirements enforced (user choice)

3. **Storage**:
   - Plain text passwords never stored
   - Only bcrypt hash stored in database
   - Hash never exposed in API responses

### Token Security

1. **JWT Configuration**:
   - Algorithm: HS256 (HMAC with SHA-256)
   - Secret key: Stored in environment variable
   - Expiration: 30 minutes (configurable)

2. **Token Payload**:
   - Contains user_id and username
   - Does not contain sensitive information
   - Includes expiration and issued-at timestamps

3. **Token Transmission**:
   - Sent in Authorization header: `Bearer <token>`
   - Should be transmitted over HTTPS in production
   - Stored in browser localStorage or sessionStorage

### Data Validation

1. **Input Validation**:
   - Email format validated with regex
   - Username length validated (3-150 chars)
   - Password length validated (8-72 chars)

2. **Uniqueness Checks**:
   - Username must be unique
   - Email must be unique
   - Checked before account creation

3. **SQL Injection Prevention**:
   - Using SQLModel ORM (parameterized queries)
   - No raw SQL queries with user input

---

## Database Migrations

**Current State**: Tables created automatically on application startup via SQLModel.

**Migration Strategy** (for future):
- Use Alembic for database migrations
- Version control all schema changes
- Test migrations in development before production

**No migrations required for 503 fix** - this is a configuration issue only.

---

## Summary

### Existing Models (No Changes Required)
- ✅ User model properly defined with all required fields
- ✅ Authentication schemas (UserCreate, UserRead, UserSignIn) properly defined
- ✅ Password hashing and JWT token handling properly implemented
- ✅ Error responses follow FastAPI conventions

### Proposed Enhancements (Optional)
- 📋 Enhanced health check response with detailed metrics
- 📋 Database latency measurement
- 📋 Endpoint availability status

### Data Model Quality
- **Security**: Excellent (bcrypt, JWT, no sensitive data exposure)
- **Validation**: Good (email format, password length, uniqueness checks)
- **Documentation**: Complete (all schemas documented with examples)
- **Maintainability**: Good (clear separation of concerns, type hints)

---

**Data Model Documentation Complete** ✅

No changes to data models are required for fixing the 503 error. All existing models are properly designed and implemented.
