# Data Model: Authentication Token and User Identification

## Entities

### Access Token
- **entity**: Access Token
- **fields**:
  - id: string (JWT token identifier)
  - user_id: string (authenticated user identifier from token)
  - issued_at: timestamp (token creation time)
  - expires_at: timestamp (token expiration time)
  - issuer: string (token issuer - Phase II system)
  - audience: string (intended audience - Phase III API)
  - scopes: array<string> (authorized permissions)
  - claims: object (additional token claims)
- **validation**:
  - Must have valid JWT format
  - Must not be expired (expires_at > current_time)
  - Signature must be valid
  - Required claims must be present

### User Identity
- **entity**: User Identity
- **fields**:
  - user_id: string (unique user identifier)
  - username: string (user display name)
  - email: string (user email address)
  - created_at: timestamp (account creation time)
  - last_login: timestamp (last authentication time)
  - roles: array<string> (user roles and permissions)
- **validation**:
  - user_id must match the one in the access token
  - Must exist in the user database

### Authentication Session
- **entity**: Authentication Session
- **fields**:
  - session_id: string (unique session identifier)
  - user_id: string (associated user)
  - token_used: string (the JWT token used for authentication)
  - authenticated_at: timestamp (authentication time)
  - expires_at: timestamp (session expiration)
  - ip_address: string (client IP address)
  - user_agent: string (client user agent string)
- **validation**:
  - Session must be active (expires_at > current_time)
  - Token must be valid for this session

## Relationships
- One Access Token belongs to one User Identity
- One User Identity can have multiple Authentication Sessions
- Authentication Session references the Access Token used

## State Transitions
- Access Token: VALID → EXPIRED (based on expires_at)
- Authentication Session: ACTIVE → EXPIRED (based on session timeout)