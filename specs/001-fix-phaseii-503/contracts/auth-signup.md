# API Contract: POST /auth/signup

**Endpoint**: `POST /auth/signup`
**Purpose**: Register a new user account
**Authentication**: Not required
**Implementation**: `phaseII/backend/app/routes/auth.py:21-101`

---

## Request

### Headers

| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Content-Type` | `application/json` | Yes | Request body format |

### Body Schema

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Field Specifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `username` | String | Min: 3, Max: 150, Required | Desired username (must be unique) |
| `email` | String | Valid email format, Required | User's email address (must be unique) |
| `password` | String | Min: 8, Max: 72, Required | Plain text password (will be hashed) |

### Validation Rules

1. **Username**:
   - Length: 3-150 characters
   - Must be unique (case-sensitive)
   - No special format requirements

2. **Email**:
   - Must match regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
   - Must be unique (case-insensitive)
   - Examples: `user@example.com`, `john.doe@company.co.uk`

3. **Password**:
   - Length: 8-72 characters (bcrypt limitation)
   - No complexity requirements enforced
   - Will be hashed with bcrypt (12 rounds) before storage

### Example Request

```bash
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

---

## Response

### Success Response (201 Created)

**Status Code**: `201 Created`

**Body Schema**:

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

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Unique user identifier (auto-generated) |
| `username` | String | User's username |
| `email` | String | User's email address |
| `created_at` | String (ISO 8601) | Account creation timestamp (UTC) |
| `updated_at` | String (ISO 8601) | Last update timestamp (UTC) |
| `is_active` | Boolean | Account active status (always true for new accounts) |

**Security Note**: The `hashed_password` field is never included in the response.

### Example Success Response

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2026-02-07T10:30:00.123456Z",
  "updated_at": "2026-02-07T10:30:00.123456Z",
  "is_active": true
}
```

---

## Error Responses

### 400 Bad Request - Invalid Email Format

**Status Code**: `400 Bad Request`

**Body**:
```json
{
  "detail": "Invalid email format"
}
```

**Cause**: Email does not match the required format.

**Example**:
```bash
# Request with invalid email
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "invalid-email",
    "password": "SecurePass123!"
  }'
```

---

### 400 Bad Request - Validation Error

**Status Code**: `400 Bad Request`

**Body**:
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 8 characters",
      "input": "short",
      "ctx": {
        "min_length": 8
      }
    }
  ]
}
```

**Cause**: Request body fails Pydantic validation (e.g., password too short, missing required fields).

**Common Validation Errors**:
- Password less than 8 characters
- Password more than 72 characters
- Username less than 3 characters
- Username more than 150 characters
- Missing required fields

---

### 409 Conflict - Username Already Exists

**Status Code**: `409 Conflict`

**Body**:
```json
{
  "detail": "Username already registered"
}
```

**Cause**: A user with the provided username already exists in the database.

**Resolution**: Choose a different username.

---

### 409 Conflict - Email Already Exists

**Status Code**: `409 Conflict`

**Body**:
```json
{
  "detail": "Email already registered"
}
```

**Cause**: A user with the provided email already exists in the database.

**Resolution**: Use a different email address or sign in with existing account.

---

### 500 Internal Server Error

**Status Code**: `500 Internal Server Error`

**Body**:
```json
{
  "detail": "An unexpected error occurred during registration"
}
```

**Cause**: Unexpected server error (e.g., database connection failure, internal exception).

**Resolution**: Check server logs for details. Retry the request.

---

## Business Logic

### Account Creation Process

1. **Validate Email Format**: Check if email matches required regex pattern
2. **Check Username Uniqueness**: Query database for existing username
3. **Check Email Uniqueness**: Query database for existing email
4. **Hash Password**: Use bcrypt with 12 rounds to hash the plain text password
5. **Create User Record**: Insert new user into database with:
   - Generated user ID (auto-increment)
   - Provided username and email
   - Hashed password
   - Current timestamp for created_at and updated_at
   - is_active set to true
6. **Return User Data**: Return UserRead schema (excludes hashed_password)

### Security Considerations

1. **Password Security**:
   - Plain text password never stored
   - Bcrypt with 12 rounds (computationally expensive)
   - Automatic salt generation

2. **Data Validation**:
   - Email format validated before database check
   - Uniqueness checks prevent duplicate accounts
   - All inputs sanitized by Pydantic

3. **Error Messages**:
   - Generic error messages for server errors
   - Specific messages for validation errors
   - No sensitive information leaked in errors

### Database Operations

```sql
-- Check for existing username
SELECT * FROM user WHERE username = 'johndoe';

-- Check for existing email
SELECT * FROM user WHERE email = 'john@example.com';

-- Insert new user
INSERT INTO user (username, email, hashed_password, created_at, updated_at, is_active)
VALUES ('johndoe', 'john@example.com', '$2b$12$...', NOW(), NOW(), true);
```

---

## Testing

### Test Cases

1. **Happy Path**: Valid signup with unique username and email
   - Expected: 201 Created with user data

2. **Invalid Email Format**: Signup with malformed email
   - Expected: 400 Bad Request with "Invalid email format"

3. **Password Too Short**: Signup with password < 8 characters
   - Expected: 400 Bad Request with validation error

4. **Password Too Long**: Signup with password > 72 characters
   - Expected: 400 Bad Request with validation error

5. **Duplicate Username**: Signup with existing username
   - Expected: 409 Conflict with "Username already registered"

6. **Duplicate Email**: Signup with existing email
   - Expected: 409 Conflict with "Email already registered"

7. **Missing Required Fields**: Signup without username, email, or password
   - Expected: 400 Bad Request with validation error

8. **Database Connection Failure**: Signup when database is unavailable
   - Expected: 500 Internal Server Error

### Example Test Script

```bash
#!/bin/bash

# Test 1: Valid signup
echo "Test 1: Valid signup"
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "email": "test1@example.com",
    "password": "SecurePass123!"
  }'

# Test 2: Duplicate username
echo "\nTest 2: Duplicate username"
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "email": "test2@example.com",
    "password": "SecurePass123!"
  }'

# Test 3: Invalid email
echo "\nTest 3: Invalid email"
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "invalid-email",
    "password": "SecurePass123!"
  }'

# Test 4: Password too short
echo "\nTest 4: Password too short"
curl -X POST http://localhost:8001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser3",
    "email": "test3@example.com",
    "password": "short"
  }'
```

---

## Rate Limiting

**Current Implementation**: None

**Recommendation**: Implement rate limiting to prevent abuse:
- Limit: 5 signup attempts per IP per hour
- Response: 429 Too Many Requests

---

## CORS Configuration

**Required Headers**:
- `Access-Control-Allow-Origin`: Frontend origin (e.g., `http://localhost:3001`)
- `Access-Control-Allow-Methods`: `POST, OPTIONS`
- `Access-Control-Allow-Headers`: `Content-Type`

**Preflight Request** (OPTIONS):
```bash
curl -X OPTIONS http://localhost:8001/auth/signup \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

---

## Performance

**Expected Response Time**: < 500ms under normal load

**Factors Affecting Performance**:
- Bcrypt hashing (computationally expensive by design)
- Database queries (username and email uniqueness checks)
- Network latency

**Optimization Opportunities**:
- Database indexes on username and email columns
- Connection pooling for database
- Caching for frequently accessed data (not applicable for signup)

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-07 | 1.0 | Initial API contract documentation |

---

**Contract Status**: ✅ Complete and Implemented
