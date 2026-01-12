# Specification: Frontend–Backend Authentication Integration using JWT (Hackathon-II Phase-II)

## 1. Existing System Review

### 1.1 Backend Authentication Endpoints
The backend authentication system is fully implemented with:
- **POST /auth/signup**: Creates new user account with username, email, and password
  - Request body: `{username: string, email: string, password: string}`
  - Response: `UserRead` object with user details (excluding sensitive information)
  - Validation: Email format, username/email uniqueness, password length (8-72 chars)
  - Error responses: 400 (invalid format), 409 (conflict), 422 (validation)

- **POST /auth/signin**: Authenticates user and returns JWT token
  - Request body: `{username: string, password: string}` (accepts username or email)
  - Response: `{access_token: string, token_type: "bearer", user_id: number, username: string}`
  - Error responses: 401 (invalid credentials), 422 (validation)

### 1.2 Frontend Structure
The existing frontend contains:
- **Pages**: `/login`, `/signup`, `/dashboard` (protected)
- **Components**: `LoginForm`, `SignupForm` using Better Auth
- **Types**: `User`, `Session`, `AuthCredentials`, `SignupData`
- **Configuration**: API URL at `http://localhost:8000` via NEXT_PUBLIC_API_URL

## 2. API Contract Definition

### 2.1 Signup Endpoint
```
POST /auth/signup
Headers: Content-Type: application/json
Request Body: {
  "username": string (3-150 chars),
  "email": string (valid email format),
  "password": string (8-72 chars)
}
Success Response: 201 Created
{
  "id": number,
  "username": string,
  "email": string,
  "created_at": string (ISO 8601),
  "updated_at": string (ISO 8601),
  "is_active": boolean
}
Error Responses:
- 400: Invalid email format
- 409: Username or email already registered
- 422: Validation errors (password length, etc.)
```

### 2.2 Signin Endpoint
```
POST /auth/signin
Headers: Content-Type: application/json
Request Body: {
  "username": string (can be username or email),
  "password": string
}
Success Response: 200 OK
{
  "access_token": string (JWT),
  "token_type": "bearer",
  "user_id": number,
  "username": string
}
Error Responses:
- 401: Incorrect username or password
- 422: Validation errors
```

### 2.3 Authorization Header Format
All protected endpoints require:
```
Authorization: Bearer <jwt_token_here>
```

## 3. Frontend Auth Service Design

### 3.1 Service Module (services/auth.ts)
```typescript
// Centralized authentication service
export interface SignupData {
  username: string;
  email: string;
  password: string;
}

export interface SigninData {
  username: string; // Can be username or email
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  username: string;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

class AuthService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  async signup(data: SignupData): Promise<UserResponse>;
  async signin(data: SigninData): Promise<AuthResponse>;
  async logout(): void;
  async getCurrentUser(token: string): Promise<UserResponse>;
  getToken(): string | null;
  setToken(token: string): void;
  removeToken(): void;
  isAuthenticated(): boolean;
}
```

### 3.2 Centralized Error Handling
The service will handle:
- Network errors
- HTTP status codes (400, 401, 409, 500, etc.)
- Parse error messages from backend responses
- Return consistent error objects to UI layer

## 4. Token Management Strategy

### 4.1 Storage Method
- **localStorage**: Store JWT token in localStorage as `auth_token`
- **Security**: Acceptable for Phase-II demo, with awareness of XSS risks
- **Alternative consideration**: sessionStorage for shorter-lived tokens

### 4.2 Token Lifecycle Management
- Store token on successful signin
- Include token in Authorization header for protected API calls
- Remove token on logout
- Check token validity before making protected requests
- Handle token expiration gracefully

## 5. Frontend Integration Plan

### 5.1 Replace Better Auth Implementation
- Remove Better Auth dependencies and configurations
- Replace `authClient` with custom JWT-based authentication service
- Update `LoginForm` to use new signin function
- Update `SignupForm` to use new signup function

### 5.2 Form Updates
- Modify `SignupForm` to accept username instead of name
- Adjust form validation to match backend requirements (username 3-150 chars)
- Display backend validation errors appropriately
- Handle success redirects after authentication

### 5.3 Protected Route Implementation
- Update `ProtectedRoute` component to check for JWT token
- Redirect to login if no valid token exists
- Optionally verify token validity with backend endpoint

## 6. Testing & Validation

### 6.1 Manual Test Cases
- **Signup Flow**: Enter valid data → User created in DB → Success response
- **Signin Flow**: Enter valid credentials → JWT received → User redirected to dashboard
- **Authenticated Request**: Access protected endpoint → Token sent → Success response
- **Invalid Token**: Send expired/invalid token → 401 response → Redirect to login
- **Validation Errors**: Enter invalid data → Backend validation errors → Display to user
- **Duplicate Registration**: Attempt duplicate signup → Conflict error → Display to user

### 6.2 Integration Verification
- Frontend signup form connects to backend /auth/signup
- Frontend signin form connects to backend /auth/signin
- JWT token properly stored and sent with protected requests
- Protected routes properly restrict access based on token validity

## 7. Implementation Phases

### Phase 1: Service Layer
- Create auth service with signup/signin/logout methods
- Implement token management utilities
- Add centralized error handling

### Phase 2: Form Integration
- Update signup form to use new auth service
- Update signin form to use new auth service
- Add proper error display and validation

### Phase 3: Protected Routes
- Update protected route component to use JWT validation
- Add token verification for protected API calls
- Implement logout functionality

### Phase 4: Testing & Polish
- Test all authentication flows end-to-end
- Handle edge cases and error scenarios
- Update documentation

## 8. Security Considerations

### 8.1 Client-Side Security
- Never expose JWT in URL parameters
- Sanitize user input before sending to backend
- Use HTTPS in production (SSL required by backend)
- Clear tokens on logout

### 8.2 Token Security
- JWT has expiration time (30 minutes by default)
- Tokens stored only in localStorage (awareness of XSS risk)
- Authorization header used for all protected requests

## 9. Quality Validation Criteria

### 9.1 Code Quality
- No hardcoded credentials or URLs
- JWT always sent via Authorization header
- Clean separation between UI and service layers
- Consistent error handling across all auth operations
- Proper TypeScript typing for all interfaces

### 9.2 User Experience
- Clear error messages from backend validation
- Loading states during authentication operations
- Smooth redirects after successful authentication
- Graceful handling of authentication failures

## 10. Out of Scope
- Refresh token implementation
- Multi-factor authentication
- Social login providers
- Password reset functionality
- Advanced role-based access control

## 11. Deliverables

1. **Auth Service Module**: `services/auth.ts` with complete JWT implementation
2. **Integrated Forms**: Updated signup and signin forms using new auth service
3. **Protected Routes**: Working protected route component with JWT validation
4. **Documentation**: Updated README explaining the authentication flow
5. **Test Results**: Verification of all authentication flows working end-to-end

## 12. Success Criteria

- [ ] Frontend signup form successfully registers users via backend API
- [ ] Frontend signin form successfully authenticates users and receives JWT
- [ ] JWT tokens properly stored and used for protected API calls
- [ ] Protected routes properly restrict access based on token validity
- [ ] All authentication flows work end-to-end without Better Auth
- [ ] Error handling displays meaningful messages from backend
- [ ] Application follows security best practices for JWT management