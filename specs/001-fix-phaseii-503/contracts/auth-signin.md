# API Contract: POST /auth/signin

**Endpoint**: `POST /auth/signin`
**Purpose**: Authenticate a user and return an access token
**Authentication**: Not required
**Implementation**: `phaseII/backend/app/routes/auth.py:104-136`

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
  "password": "string"
}
```

### Field Specifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `username` | String | Required | Username or email address |
| `password` | String | Required | Plain text password |

### Validation Rules

1. **Username**:
   - Can be either username or email address
   - Case-sensitive for username
   - Case-insensitive for email
   - No length restrictions (validated against database)

2. **Password**:
   - Plain text password
   - Will be verified against stored bcrypt hash
   - No length restrictions on signin (only on signup)

### Example Request

```bash
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
```

### Alternative Request (Using Email)

```bash
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john@example.com",
    "password": "SecurePass123!"
  }'
```

---

## Response

### Success Response (200 OK)

**Status Code**: `200 OK`

**Body Schema**:

```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user_id": 1,
  "username": "string"
}
```

**Field Descriptions**:

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | String | JWT access token for authenticated requests |
| `token_type` | String | Token type (always "bearer") |
| `user_id` | Integer | User's unique identifier |
| `username` | String | User's username |

**JWT Token Details**:
- Algorithm: HS256
- Expiration: 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
- Payload includes: `sub` (user_id), `user_id`, `username`, `exp`, `iat`

### Example Success Response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJqb2huZG9lIiwiZXhwIjoxNzA3MzExNDAwLCJpYXQiOjE3MDczMDk2MDB9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
  "token_type": "bearer",
  "user_id": 1,
  "username": "johndoe"
}
```

**Token Usage**:
```bash
# Use token in subsequent requests
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Error Responses

### 401 Unauthorized - Invalid Credentials

**Status Code**: `401 Unauthorized`

**Headers**:
```
WWW-Authenticate: Bearer
```

**Body**:
```json
{
  "detail": "Incorrect username or password"
}
```

**Cause**: Username/email not found or password does not match.

**Security Note**: The error message is intentionally generic to prevent username enumeration attacks.

**Example**:
```bash
# Request with wrong password
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "WrongPassword123!"
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
      "type": "missing",
      "loc": ["body", "password"],
      "msg": "Field required",
      "input": {
        "username": "johndoe"
      }
    }
  ]
}
```

**Cause**: Request body fails Pydantic validation (e.g., missing required fields).

**Common Validation Errors**:
- Missing username field
- Missing password field
- Invalid JSON format

---

### 500 Internal Server Error

**Status Code**: `500 Internal Server Error`

**Body**:
```json
{
  "detail": "An unexpected error occurred during authentication"
}
```

**Cause**: Unexpected server error (e.g., database connection failure, internal exception).

**Resolution**: Check server logs for details. Retry the request.

---

## Business Logic

### Authentication Process

1. **Find User**: Query database for user by username or email
   - SQL: `SELECT * FROM user WHERE username = ? OR email = ?`
   - Case-sensitive for username, case-insensitive for email

2. **Verify Password**: Compare provided password with stored bcrypt hash
   - Uses `bcrypt.checkpw()` for secure comparison
   - Constant-time comparison to prevent timing attacks

3. **Create Access Token**: Generate JWT token with user information
   - Payload: `{"sub": user_id, "user_id": user_id, "username": username}`
   - Expiration: Current time + 30 minutes
   - Signed with secret key from environment variable

4. **Return Token**: Return access token with user information

### Security Considerations

1. **Password Verification**:
   - Uses bcrypt for secure password comparison
   - Constant-time comparison prevents timing attacks
   - No password information leaked in error messages

2. **Error Messages**:
   - Generic error message for invalid credentials
   - Prevents username enumeration attacks
   - No distinction between "user not found" and "wrong password"

3. **Token Security**:
   - JWT signed with secret key
   - Expiration time enforced
   - Token should be transmitted over HTTPS in production

4. **Account Status**:
   - Only active accounts can sign in (is_active = true)
   - Inactive accounts return same error as invalid credentials

### Database Operations

```sql
-- Find user by username or email
SELECT * FROM user
WHERE username = 'johndoe' OR email = 'johndoe'
LIMIT 1;

-- Password verification happens in application code (bcrypt)
-- Token generation happens in application code (JWT)
```

---

## Testing

### Test Cases

1. **Happy Path - Username**: Valid signin with username
   - Expected: 200 OK with access token

2. **Happy Path - Email**: Valid signin with email
   - Expected: 200 OK with access token

3. **Invalid Username**: Signin with non-existent username
   - Expected: 401 Unauthorized

4. **Invalid Password**: Signin with wrong password
   - Expected: 401 Unauthorized

5. **Missing Username**: Signin without username field
   - Expected: 400 Bad Request with validation error

6. **Missing Password**: Signin without password field
   - Expected: 400 Bad Request with validation error

7. **Empty Credentials**: Signin with empty strings
   - Expected: 401 Unauthorized

8. **Database Connection Failure**: Signin when database is unavailable
   - Expected: 500 Internal Server Error

9. **Token Expiration**: Use expired token for authenticated request
   - Expected: 401 Unauthorized

### Example Test Script

```bash
#!/bin/bash

# Test 1: Valid signin with username
echo "Test 1: Valid signin with username"
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'

# Test 2: Valid signin with email
echo "\nTest 2: Valid signin with email"
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john@example.com",
    "password": "SecurePass123!"
  }'

# Test 3: Invalid password
echo "\nTest 3: Invalid password"
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "WrongPassword"
  }'

# Test 4: Non-existent user
echo "\nTest 4: Non-existent user"
curl -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nonexistent",
    "password": "SomePassword123!"
  }'

# Test 5: Use token for authenticated request
echo "\nTest 5: Use token for authenticated request"
TOKEN=$(curl -s -X POST http://localhost:8001/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }' | jq -r '.access_token')

curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## Rate Limiting

**Current Implementation**: None

**Recommendation**: Implement rate limiting to prevent brute force attacks:
- Limit: 5 failed signin attempts per IP per 15 minutes
- Response: 429 Too Many Requests
- Consider account lockout after 10 failed attempts

---

## CORS Configuration

**Required Headers**:
- `Access-Control-Allow-Origin`: Frontend origin (e.g., `http://localhost:3001`)
- `Access-Control-Allow-Methods`: `POST, OPTIONS`
- `Access-Control-Allow-Headers`: `Content-Type`

**Preflight Request** (OPTIONS):
```bash
curl -X OPTIONS http://localhost:8001/auth/signin \
  -H "Origin: http://localhost:3001" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
```

---

## Performance

**Expected Response Time**: < 300ms under normal load

**Factors Affecting Performance**:
- Bcrypt password verification (computationally expensive by design)
- Database query (user lookup)
- JWT token generation
- Network latency

**Optimization Opportunities**:
- Database index on username and email columns
- Connection pooling for database
- Token caching (not recommended for security reasons)

---

## Token Management

### Token Lifecycle

1. **Creation**: Token created on successful signin
2. **Storage**: Client stores token (localStorage or sessionStorage)
3. **Usage**: Client includes token in Authorization header for authenticated requests
4. **Expiration**: Token expires after 30 minutes
5. **Refresh**: User must sign in again after expiration (no refresh token implemented)

### Token Validation

**Endpoint**: `GET /auth/me`
**Purpose**: Validate token and get current user information

**Request**:
```bash
curl -X GET http://localhost:8001/auth/me \
  -H "Authorization: Bearer <access_token>"
```

**Response** (200 OK):
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

---

## Security Best Practices

1. **Always use HTTPS in production** to prevent token interception
2. **Store tokens securely** (avoid localStorage if XSS is a concern)
3. **Implement token refresh** for better user experience
4. **Add rate limiting** to prevent brute force attacks
5. **Log failed signin attempts** for security monitoring
6. **Consider multi-factor authentication** for sensitive applications

---

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-02-07 | 1.0 | Initial API contract documentation |

---

**Contract Status**: ✅ Complete and Implemented
