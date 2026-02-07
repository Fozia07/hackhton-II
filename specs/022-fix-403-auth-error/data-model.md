# Data Model: Authentication Identity Fix

## Entity: UserIdentity
- **Fields**:
  - id: string (unique identifier from backend)
  - username: string (canonical username for API calls)
  - email: string (user's email address, optional)
  - token_username: string (username claim from JWT token)
  - stored_username: string (username stored in localStorage)

- **Validation Rules**:
  - username must match the format expected by the backend
  - token_username must match stored_username for successful API calls
  - email, if present, may need normalization to username format

## Entity: AuthenticationSession
- **Fields**:
  - jwt_token: string (encoded JWT token)
  - login_input: string (what user entered during login)
  - canonical_username: string (actual username for API calls)
  - storage_timestamp: datetime (when credentials were stored)

- **State Transitions**:
  - Login Initiated → Login Successful → Credentials Stored
  - Login Initiated → Login Successful → Identity Normalized
  - Login Initiated → Login Failed → Error Returned

## Entity: APIRequest
- **Fields**:
  - endpoint: string (API endpoint being called)
  - path_params: object (parameters in URL path)
  - auth_header: string (authorization header with JWT)
  - user_identifier: string (username used in path parameter)

- **Validation Rules**:
  - user_identifier in path must match username in JWT token
  - auth_header must contain valid JWT token
  - path_params must conform to backend expectations

## Relationships
- AuthenticationSession (1) → UserIdentity (1) : "creates"
- APIRequest (N) ← AuthenticationSession (1) : "initiates"