# Research: Fix Frontend-Backend Auth Integration Errors

## Research Findings

### 1. Error Analysis

**Error A: "Failed to fetch" during login/signup**
- **Root Cause**: Likely CORS (Cross-Origin Resource Sharing) misconfiguration
- **Evidence**: Backend is running but frontend cannot make requests due to CORS policy
- **Solution**: Configure backend to allow requests from frontend origin

**Error B: Dashboard 404 after successful login**
- **Root Cause**: ProtectedRoute component not properly handling authentication state or redirect logic
- **Evidence**: User authenticates but cannot access protected dashboard route
- **Solution**: Fix ProtectedRoute logic and ensure proper token handling

**Error C: AuthContext import/type error**
- **Root Cause**: Missing or incorrect import path for User type
- **Evidence**: Import statement `import { User } from '../types/auth'` failing
- **Solution**: Verify types/auth.ts file exists and path is correct

### 2. System Architecture Understanding

**Backend Stack:**
- FastAPI with JWT authentication
- Neon PostgreSQL database
- CORS middleware configuration
- Auth endpoints: /auth/signup, /auth/signin, /auth/me

**Frontend Stack:**
- Next.js App Router
- Custom JWT authentication service
- AuthContext for state management
- ProtectedRoute component for route protection
- Todo API endpoints: /todos (GET, POST, PUT, DELETE)

### 3. Integration Points

**API Communication Flow:**
1. Frontend makes auth requests to backend via NEXT_PUBLIC_API_URL
2. Backend returns JWT token on successful authentication
3. Frontend stores token in localStorage
4. Frontend sends token in Authorization header for protected requests
5. Backend validates JWT for protected endpoints

### 4. Known Issues & Solutions

**CORS Configuration Issue:**
- Problem: Frontend (port 3000+) cannot access backend (port 8000) due to CORS policy
- Solution: Update backend CORS settings to allow frontend origin

**Token Management Issue:**
- Problem: JWT token may not be properly stored or sent with requests
- Solution: Verify token storage and retrieval in auth service

**Route Protection Issue:**
- Problem: ProtectedRoute may not be correctly checking authentication state
- Solution: Fix authentication state checking and redirect logic

**Todo API Integration:**
- Problem: Todo endpoints require authentication but may not be properly secured
- Solution: Ensure all Todo endpoints validate JWT tokens

## Decision Log

### Decision: CORS Configuration Strategy
- **Rationale**: The most common cause of "Failed to fetch" errors in local development is CORS misconfiguration
- **Chosen Approach**: Configure backend to allow all origins during development (*)
- **Alternatives Considered**:
  - Specific origin whitelisting (more secure but requires exact port matching)
  - Proxy configuration (adds complexity)

### Decision: Auth State Management
- **Rationale**: Proper authentication state management is crucial for protecting routes
- **Chosen Approach**: Use AuthContext with loading, authenticated, and error states
- **Alternatives Considered**:
  - Local storage only (less secure, no loading states)
  - Session storage only (expires on tab close)

### Decision: Error Handling Strategy
- **Rationale**: Clear error messages improve user experience and debugging
- **Chosen Approach**: Specific error messages instead of generic "Failed to fetch"
- **Alternatives Considered**:
  - Generic error handling (harder to debug)
  - Console-only errors (not visible to users)

## Technical Unknowns Resolved

1. **CORS Configuration**: Backend CORS settings need to be updated
2. **AuthContext Path**: Need to verify existence of types/auth.ts file
3. **ProtectedRoute Logic**: Need to examine current authentication checking implementation
4. **API URL Configuration**: Verify NEXT_PUBLIC_API_URL is correctly set
5. **JWT Token Handling**: Verify token storage and retrieval mechanisms