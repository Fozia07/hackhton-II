# JWT & Better Auth Integration

## Expertise
Expert skill for integrating Better Auth (Next.js frontend) with FastAPI backend using stateless JWT authentication. Specializes in secure token issuance, verification, user identity extraction, and authorization enforcement across frontend and backend boundaries.

## Purpose
This skill handles authentication integration between Next.js and FastAPI, enabling you to:
- Configure Better Auth to issue JWT tokens
- Attach JWT tokens to all backend API requests
- Verify JWT tokens in FastAPI endpoints
- Extract authenticated user identity from tokens
- Enforce user-level authorization
- Handle authentication errors gracefully
- Maintain stateless authentication across services

## When to Use
Use this skill when you need to:
- Set up authentication between Next.js and FastAPI
- Configure Better Auth JWT plugin
- Implement JWT verification in FastAPI
- Create reusable auth dependencies
- Enforce user-level access controls
- Handle token expiry and refresh
- Secure API endpoints with JWT
- Extract user identity from tokens

## Core Concepts

### Authentication Flow

```
1. User logs in via Better Auth (Next.js)
   ↓
2. Better Auth issues JWT token
   ↓
3. Frontend stores token (httpOnly cookie or localStorage)
   ↓
4. Frontend attaches token to API requests
   Authorization: Bearer <token>
   ↓
5. FastAPI verifies JWT signature and claims
   ↓
6. FastAPI extracts user_id/email from token
   ↓
7. FastAPI processes request with user context
   ↓
8. FastAPI returns response
```

### JWT Token Structure

```json
{
  "sub": "user_123",           // User ID (subject)
  "email": "user@example.com", // User email
  "exp": 1704672000,           // Expiration timestamp
  "iat": 1704668400            // Issued at timestamp
}
```

## Frontend Implementation (Next.js + Better Auth)

### 1. Better Auth Configuration

**Install Better Auth**:
```bash
npm install better-auth
```

**Configure Better Auth with JWT** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  // Database configuration
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL!,
  },

  // Email provider (optional)
  emailAndPassword: {
    enabled: true,
  },

  // JWT Plugin Configuration
  plugins: [
    jwt({
      // JWT secret from environment
      secret: process.env.BETTER_AUTH_SECRET!,

      // Token expiration (1 hour)
      expiresIn: "1h",

      // Algorithm
      algorithm: "HS256",

      // Include user data in token
      payload: async (user) => ({
        sub: user.id,
        email: user.email,
      }),
    }),
  ],

  // Session configuration
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
});

export type Session = typeof auth.$Infer.Session;
```

**Environment Variables** (`.env.local`):
```bash
# Better Auth Secret (minimum 32 characters)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-in-production

# Database URL
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Better Auth API Route

**Create Auth API Route** (`app/api/auth/[...all]/route.ts`):
```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### 3. Client-Side Auth Hook

**Create Auth Client** (`lib/auth-client.ts`):
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
```

### 4. Fetching with JWT Token

**API Client with JWT** (`lib/api-client.ts`):
```typescript
import { authClient } from "./auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get JWT token from Better Auth session.
 */
async function getJWTToken(): Promise<string | null> {
  try {
    const session = await authClient.getSession();

    if (!session?.data?.session) {
      return null;
    }

    // Get JWT token from Better Auth
    const response = await fetch("/api/auth/get-jwt", {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      return null;
    }

    const data = await response.json();
    return data.token;
  } catch (error) {
    console.error("Failed to get JWT token:", error);
    return null;
  }
}

/**
 * Fetch wrapper that automatically attaches JWT token.
 */
export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // Get JWT token
  const token = await getJWTToken();

  // Prepare headers
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Attach JWT token if available
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  // Make request
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Handle authentication errors
  if (response.status === 401) {
    // Token expired or invalid - redirect to login
    window.location.href = "/login";
    throw new Error("Authentication required");
  }

  if (response.status === 403) {
    throw new Error("Access denied");
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

/**
 * API client methods.
 */
export const api = {
  get: <T>(endpoint: string) => apiFetch<T>(endpoint, { method: "GET" }),

  post: <T>(endpoint: string, data?: any) =>
    apiFetch<T>(endpoint, {
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    }),

  put: <T>(endpoint: string, data?: any) =>
    apiFetch<T>(endpoint, {
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    }),

  delete: <T>(endpoint: string) =>
    apiFetch<T>(endpoint, { method: "DELETE" }),
};
```

**JWT Token Endpoint** (`app/api/auth/get-jwt/route.ts`):
```typescript
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    // Get session from Better Auth
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session?.user) {
      return NextResponse.json(
        { error: "Not authenticated" },
        { status: 401 }
      );
    }

    // Generate JWT token
    const token = await auth.api.signJWT({
      payload: {
        sub: session.user.id,
        email: session.user.email,
      },
    });

    return NextResponse.json({ token });
  } catch (error) {
    console.error("Failed to generate JWT:", error);
    return NextResponse.json(
      { error: "Failed to generate token" },
      { status: 500 }
    );
  }
}
```

### 5. Using API Client in Components

**Example: Fetching User Data**:
```typescript
"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api-client";
import { useSession } from "@/lib/auth-client";

interface UserProfile {
  id: string;
  email: string;
  username: string;
}

export function UserProfile() {
  const { data: session } = useSession();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProfile() {
      if (!session?.user) {
        setLoading(false);
        return;
      }

      try {
        const data = await api.get<UserProfile>("/api/v1/users/me");
        setProfile(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load profile");
      } finally {
        setLoading(false);
      }
    }

    fetchProfile();
  }, [session]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!profile) return <div>Not authenticated</div>;

  return (
    <div>
      <h2>Profile</h2>
      <p>Email: {profile.email}</p>
      <p>Username: {profile.username}</p>
    </div>
  );
}
```

## Backend Implementation (FastAPI)

### 1. JWT Configuration

**Install Dependencies**:
```bash
pip install python-jose[cryptography]
pip install python-multipart
```

**JWT Configuration** (`core/config.py`):
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    # Better Auth Secret (must match frontend)
    better_auth_secret: str = Field(..., min_length=32)

    # JWT Configuration
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60

    # Database
    database_url: str = Field(...)

    # API
    api_v1_prefix: str = "/api/v1"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**Environment Variables** (`.env`):
```bash
# Better Auth Secret (MUST match frontend)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars-change-in-production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

### 2. JWT Verification

**JWT Utilities** (`core/jwt.py`):
```python
from jose import jwt, JWTError
from datetime import datetime
from typing import Optional
from core.config import get_settings

settings = get_settings()

def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return payload.

    Args:
        token: JWT token string

    Returns:
        Token payload if valid, None otherwise
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=[settings.jwt_algorithm]
        )

        # Verify expiration
        exp = payload.get("exp")
        if exp is None:
            return None

        if datetime.utcnow().timestamp() > exp:
            return None

        return payload

    except JWTError:
        return None

def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID if valid, None otherwise
    """
    payload = verify_jwt_token(token)
    if payload:
        return payload.get("sub")
    return None

def get_user_email_from_token(token: str) -> Optional[str]:
    """
    Extract user email from JWT token.

    Args:
        token: JWT token string

    Returns:
        User email if valid, None otherwise
    """
    payload = verify_jwt_token(token)
    if payload:
        return payload.get("email")
    return None
```

### 3. Authentication Dependencies

**Auth Dependencies** (`core/dependencies.py`):
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from typing import Optional

from core.jwt import verify_jwt_token, get_user_id_from_token
from core.database import get_db
from models.user import User

# HTTP Bearer token scheme
security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract and verify JWT token, return user ID.

    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    token = credentials.credentials

    # Verify token
    payload = verify_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id

async def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from database.

    Raises:
        HTTPException: 401 if user not found
    """
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise.
    Use for endpoints that work with or without authentication.
    """
    if not credentials:
        return None

    try:
        user_id = await get_current_user_id(credentials)
        return db.get(User, user_id)
    except HTTPException:
        return None
```

### 4. Using Auth Dependencies in Endpoints

**Protected Endpoint Example**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.dependencies import get_current_user, get_db
from models.user import User
from schemas.user import UserResponse

router = APIRouter(prefix="/api/v1", tags=["users"])

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile.
    Requires valid JWT token.
    """
    return current_user

@router.put("/users/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.
    Users can only update their own profile.
    """
    # Update user
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    return current_user
```

**Resource Ownership Enforcement**:
```python
from models.post import Post

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get post by ID."""
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check ownership for private posts
    if post.is_private and post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You don't own this post"
        )

    return post

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update post. Only owner can update."""
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Enforce ownership
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You don't own this post"
        )

    # Update post
    for key, value in post_update.dict(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)

    return post

@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete post. Only owner can delete."""
    post = db.get(Post, post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Enforce ownership
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: You don't own this post"
        )

    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}
```

**Optional Authentication**:
```python
@router.get("/posts/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0,
    limit: int = 100,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    List posts.
    Shows public posts to everyone.
    Shows user's private posts if authenticated.
    """
    query = select(Post).offset(skip).limit(limit)

    if current_user:
        # Show public posts + user's own posts
        query = query.where(
            (Post.is_private == False) | (Post.user_id == current_user.id)
        )
    else:
        # Show only public posts
        query = query.where(Post.is_private == False)

    posts = db.execute(query).scalars().all()
    return posts
```

### 5. CORS Configuration

**Enable CORS for Frontend** (`main.py`):
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import get_settings

settings = get_settings()

app = FastAPI(title="My API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "https://yourdomain.com",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

### Frontend Error Handling

```typescript
// lib/api-client.ts
export class AuthenticationError extends Error {
  constructor(message: string = "Authentication required") {
    super(message);
    this.name = "AuthenticationError";
  }
}

export class AuthorizationError extends Error {
  constructor(message: string = "Access denied") {
    super(message);
    this.name = "AuthorizationError";
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getJWTToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    throw new AuthenticationError("Please log in to continue");
  }

  if (response.status === 403) {
    throw new AuthorizationError("You don't have permission to access this resource");
  }

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}
```

### Backend Error Handling

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )
```

## Security Best Practices

### 1. Secret Management
- Use strong secrets (minimum 32 characters)
- Never commit secrets to version control
- Use same secret in frontend and backend
- Rotate secrets regularly
- Use environment variables

### 2. Token Security
- Use HTTPS in production (wss:// for WebSockets)
- Set appropriate token expiration (1 hour recommended)
- Implement token refresh mechanism
- Store tokens securely (httpOnly cookies preferred)
- Never log tokens

### 3. Authorization
- Always verify user identity from token
- Enforce resource ownership
- Use 401 for authentication errors
- Use 403 for authorization errors
- Validate all user inputs

### 4. CORS Configuration
- Specify exact origins (avoid wildcards in production)
- Enable credentials for cookie-based auth
- Restrict allowed methods and headers
- Test CORS configuration thoroughly

## Testing

### Frontend Testing

```typescript
// __tests__/api-client.test.ts
import { api } from "@/lib/api-client";

describe("API Client", () => {
  it("should attach JWT token to requests", async () => {
    // Mock getJWTToken
    jest.mock("@/lib/api-client", () => ({
      getJWTToken: jest.fn().mockResolvedValue("mock-token"),
    }));

    // Test request
    await api.get("/api/v1/users/me");

    // Verify Authorization header
    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        headers: expect.objectContaining({
          Authorization: "Bearer mock-token",
        }),
      })
    );
  });
});
```

### Backend Testing

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from datetime import datetime, timedelta

def create_test_token(user_id: str, secret: str) -> str:
    """Create test JWT token."""
    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, secret, algorithm="HS256")

def test_protected_endpoint_without_token(client: TestClient):
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_protected_endpoint_with_valid_token(client: TestClient, test_user):
    """Test accessing protected endpoint with valid token."""
    token = create_test_token(str(test_user.id), settings.better_auth_secret)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id

def test_protected_endpoint_with_expired_token(client: TestClient):
    """Test accessing protected endpoint with expired token."""
    payload = {
        "sub": "user_123",
        "email": "test@example.com",
        "exp": datetime.utcnow() - timedelta(hours=1)  # Expired
    }
    token = jwt.encode(payload, settings.better_auth_secret, algorithm="HS256")

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 401
```

## Summary

This skill provides comprehensive guidance for integrating Better Auth (Next.js) with FastAPI using JWT authentication:

**Frontend (Next.js + Better Auth):**
- Better Auth configuration with JWT plugin
- JWT token generation endpoint
- API client with automatic token attachment
- Error handling and token refresh
- Secure token storage

**Backend (FastAPI):**
- JWT verification utilities
- Reusable authentication dependencies
- Resource ownership enforcement
- Optional authentication support
- CORS configuration

**Security:**
- Stateless JWT authentication
- Token expiration and validation
- Resource-level authorization
- Secure secret management
- Error handling best practices

Use this skill to implement secure, stateless authentication between your Next.js frontend and FastAPI backend with proper token management, authorization enforcement, and error handling for production environments.
