# Implementation Plan: Frontend-Backend JWT Authentication Integration

## Overview
This plan outlines the implementation of JWT-based authentication integration between the frontend and backend systems. The goal is to replace the existing Better Auth implementation with a custom JWT solution that connects to the backend auth endpoints.

## Phase 1: Service Layer Implementation
### 1.1 Create Auth Service Module
- [ ] Create `src/lib/auth/service.ts` file
- [ ] Implement `AuthService` class with signup, signin, logout methods
- [ ] Add token management methods (getToken, setToken, removeToken)
- [ ] Implement error handling utilities
- [ ] Add proper TypeScript interfaces for requests/responses

### 1.2 API Integration
- [ ] Implement signup method that calls `/auth/signup`
- [ ] Implement signin method that calls `/auth/signin`
- [ ] Implement logout method that clears local storage
- [ ] Add method to verify token validity
- [ ] Create HTTP utility functions for API calls

## Phase 2: Replace Better Auth Implementation
### 2.1 Update Auth Client
- [ ] Replace `src/lib/auth/client.ts` with custom implementation
- [ ] Export new auth methods (customSignUp, customSignIn, customSignOut)
- [ ] Implement useSession hook for authentication state management
- [ ] Remove Better Auth dependencies

### 2.2 Form Updates
- [ ] Update `src/components/auth/SignupForm.tsx` to use new auth service
- [ ] Modify form fields to match backend requirements (add username field)
- [ ] Update `src/components/auth/LoginForm.tsx` to use new auth service
- [ ] Adjust validation to match backend constraints
- [ ] Update error handling to display backend validation messages

## Phase 3: Protected Routes & State Management
### 3.1 Authentication Context
- [ ] Create `src/contexts/AuthContext.tsx` for global auth state
- [ ] Implement provider with login, logout, and token management
- [ ] Add loading and error states
- [ ] Export custom hook for consuming auth state

### 3.2 Protected Route Component
- [ ] Update `src/components/auth/ProtectedRoute.tsx` to use JWT validation
- [ ] Check for valid token in localStorage
- [ ] Redirect to login if no valid token exists
- [ ] Optionally verify token with backend call

## Phase 4: Integration & Testing
### 4.1 API Integration
- [ ] Connect signup form to backend API
- [ ] Connect signin form to backend API
- [ ] Implement token storage on successful authentication
- [ ] Add token validation for protected routes

### 4.2 Error Handling
- [ ] Display backend validation errors in forms
- [ ] Handle network errors gracefully
- [ ] Implement proper error messaging to users
- [ ] Add loading states during authentication operations

## Phase 5: Testing & Validation
### 5.1 Manual Testing
- [ ] Test signup flow: valid data → successful registration
- [ ] Test signin flow: valid credentials → JWT received → dashboard access
- [ ] Test validation errors: invalid data → proper error messages
- [ ] Test duplicate registration: conflict errors handled properly
- [ ] Test protected routes: no token → redirect to login

### 5.2 Edge Cases
- [ ] Token expiration handling
- [ ] Invalid token handling
- [ ] Network error handling
- [ ] Logout functionality verification

## Technical Implementation Details

### Auth Service Interface
```typescript
interface AuthService {
  signup(data: SignupData): Promise<UserResponse>;
  signin(data: SigninData): Promise<AuthResponse>;
  logout(): void;
  getToken(): string | null;
  isAuthenticated(): boolean;
  refreshToken(): Promise<string>;
}
```

### HTTP Utility Functions
- Use fetch API with proper error handling
- Include Authorization header for protected requests
- Parse JSON responses safely
- Handle different HTTP status codes appropriately

### Security Considerations
- Store JWT in localStorage (acceptable for Phase II)
- Use HTTPS in production
- Sanitize inputs before sending to backend
- Clear tokens on logout

## Dependencies & Setup
- Ensure NEXT_PUBLIC_API_URL is set correctly in .env files
- Remove Better Auth dependencies if no longer needed
- Add any missing dependencies for HTTP utilities
- Update any imports that reference old auth system

## Rollback Strategy
If issues arise during implementation:
- Keep backup of Better Auth implementation
- Use feature flags to toggle between implementations
- Revert changes if critical functionality breaks
- Test thoroughly in development before deploying