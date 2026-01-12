# Data Model: Auth Integration Fixes

## User Entity

**Definition**: Represents authenticated user with JWT token, authentication status, and user properties

**Fields**:
- `id`: number - Unique identifier for the user
- `username`: string - User's unique username
- `email`: string - User's email address
- `created_at`: string - ISO 8601 timestamp of account creation
- `updated_at`: string - ISO 8601 timestamp of last update
- `is_active`: boolean - Account status flag

## Authentication State

**Definition**: Structure holding the current authentication state across the application

**Fields**:
- `user`: User | null - Current user data if authenticated, null otherwise
- `isAuthenticated`: boolean - Flag indicating authentication status
- `isLoading`: boolean - Flag indicating authentication state is being checked
- `error`: string | null - Error message if authentication failed

## JWT Token Structure

**Definition**: Authentication token stored in localStorage with expiration handling

**Fields**:
- `access_token`: string - JWT access token string
- `token_type`: string - Type of token (usually "bearer")
- `user_id`: number - Associated user ID
- `username`: string - Associated username

## Auth Action

**Definition**: Actions that can be dispatched to the authentication reducer

**Fields**:
- `type`: string - Action type identifier
- `payload`: any (optional) - Additional data for the action

## Protected Route Props

**Definition**: Properties for the ProtectedRoute component

**Fields**:
- `children`: ReactNode - Child components to render when authenticated
- `fallback`: ReactNode (optional) - Component to render when not authenticated