# Data Model: Fix Frontend-Backend Auth Integration Errors

## Core Entities

### 1. JWT Token
- **Purpose**: Represents user authentication state
- **Fields**:
  - `access_token`: string (JWT token string)
  - `token_type`: string (e.g., "bearer")
  - `expires_in`: number (expiration time in seconds)
  - `user_id`: number (associated user ID)
  - `username`: string (associated username)

### 2. User Session
- **Purpose**: Manages authenticated state between frontend and backend
- **Fields**:
  - `user`: User object (nullable) - current authenticated user
  - `isAuthenticated`: boolean - authentication status
  - `isLoading`: boolean - loading state during auth checks
  - `error`: string (nullable) - error message if auth failed

### 3. Todo Item
- **Purpose**: Represents a task with title, description, completion status, and user association
- **Fields**:
  - `id`: number - unique identifier
  - `title`: string - task title
  - `description`: string (nullable) - task description
  - `completed`: boolean - completion status
  - `user_id`: number - foreign key to user
  - `created_at`: string (ISO 8601 timestamp) - creation time
  - `updated_at`: string (ISO 8601 timestamp) - last update time

### 4. Todo Collection
- **Purpose**: Set of Todo items belonging to a specific authenticated user
- **Relationships**:
  - Contains multiple Todo Items
  - Associated with single User via user_id

## Validation Rules

### JWT Token Validation
- Must be a valid JWT format (3 parts separated by dots)
- Must not be expired (check exp claim against current time)
- Must have valid signature when verified against backend secret

### User Session Validation
- `isAuthenticated` must be true when `user` is not null
- `isLoading` should be false when session state is determined
- `error` should be null when authentication is successful

### Todo Item Validation
- `title` must be 1-255 characters
- `description` can be null or 0-1000 characters
- `completed` defaults to false
- `user_id` must reference an existing user
- `created_at` and `updated_at` are auto-generated timestamps

## State Transitions

### User Session States
```
Initial State → Checking Auth → [Authenticated/Unauthenticated]
                              ↓
                        Authenticated → Active Session
                              ↓
                        Unauthenticated → Login Required
```

### Todo Item States
```
New Todo → Created → [Active/Completed]
                    ↓
               Active ↔ Completed
```

## API Contract Elements

### Auth API Endpoints
- `POST /auth/signup` - Create new user account
- `POST /auth/signin` - Authenticate user and return JWT
- `GET /auth/me` - Get current user profile using JWT

### Todo API Endpoints
- `GET /todos` - Get all todos for authenticated user
- `POST /todos` - Create new todo for authenticated user
- `PUT /todos/{id}` - Update existing todo for authenticated user
- `DELETE /todos/{id}` - Delete todo for authenticated user

### Expected Response Formats

#### Auth Response
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user_id": 123,
  "username": "username"
}
```

#### User Profile Response
```json
{
  "id": 123,
  "username": "username",
  "email": "user@example.com",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

#### Todo Response
```json
[
  {
    "id": 1,
    "title": "Sample Todo",
    "description": "Description of the task",
    "completed": false,
    "user_id": 123,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```