# FastAPI Validation, Error Handling & Security

## Expertise
Expert skill for ensuring FastAPI APIs are safe, validated, and reliable through comprehensive input validation, error handling, and security best practices. Specializes in Pydantic models, exception handling, CORS configuration, and API security patterns.

## Purpose
This skill handles validation, error handling, and security concerns for FastAPI applications, enabling you to:
- Define robust Pydantic models for request/response validation
- Validate all inputs (body, query, path parameters)
- Handle errors gracefully with HTTPException and custom handlers
- Implement global exception handling
- Configure CORS and security headers
- Apply authentication and authorization patterns
- Protect against common security vulnerabilities

## When to Use
Use this skill when you need to:
- Validate API request data
- Define response schemas
- Handle errors consistently across your API
- Implement authentication and authorization
- Configure CORS for frontend integration
- Secure your API against common attacks
- Add input sanitization and validation rules

## Core Concepts

### 1. Pydantic Request & Response Models

**Basic Request Model**:
```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Request model for creating a user."""
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "password": "SecurePass123!",
                "full_name": "John Doe",
                "age": 30
            }
        }
```

**Response Model**:
```python
class UserResponse(BaseModel):
    """Response model for user data."""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True  # Allows ORM model conversion
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "created_at": "2024-01-01T00:00:00",
                "is_active": True
            }
        }
```

**Nested Models**:
```python
from typing import List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str = Field(..., regex=r'^\d{5}(-\d{4})?$')

class UserWithAddress(BaseModel):
    email: EmailStr
    username: str
    addresses: List[Address] = []

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "addresses": [
                    {
                        "street": "123 Main St",
                        "city": "Springfield",
                        "state": "IL",
                        "zip_code": "62701"
                    }
                ]
            }
        }
```

### 2. Input Validation

**Custom Validators**:
```python
from pydantic import BaseModel, validator, field_validator
import re

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    confirm_password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format."""
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """Validate that passwords match."""
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
```

**Query Parameter Validation**:
```python
from fastapi import APIRouter, Query
from typing import Optional
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

router = APIRouter()

@router.get("/users")
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    search: Optional[str] = Query(None, min_length=3, max_length=100),
    sort_by: Optional[str] = Query("created_at", regex="^(username|email|created_at)$"),
    sort_order: SortOrder = Query(SortOrder.desc),
    is_active: Optional[bool] = Query(None)
):
    """
    List users with validated query parameters.
    """
    # Implementation
    pass
```

**Path Parameter Validation**:
```python
from fastapi import Path

@router.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(..., gt=0, description="User ID must be positive")
):
    """Get user by ID with validated path parameter."""
    # Implementation
    pass

@router.get("/posts/{slug}")
async def get_post(
    slug: str = Path(..., regex="^[a-z0-9-]+$", min_length=3, max_length=100)
):
    """Get post by slug with validated path parameter."""
    # Implementation
    pass
```

**Body Validation**:
```python
from fastapi import Body

@router.post("/users")
async def create_user(
    user: UserCreate = Body(..., embed=True),
    send_welcome_email: bool = Body(True)
):
    """
    Create user with validated body.
    embed=True wraps the model in a JSON object with the parameter name as key.
    """
    # Implementation
    pass
```

### 3. HTTPException Usage

**Basic HTTPException**:
```python
from fastapi import HTTPException, status

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

**HTTPException with Headers**:
```python
@router.post("/login")
async def login(credentials: LoginCredentials):
    user = await authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": create_token(user)}
```

**Custom Exception Classes**:
```python
class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

class InsufficientPermissionsException(HTTPException):
    def __init__(self, required_permission: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions. Required: {required_permission}"
        )

class ValidationException(HTTPException):
    def __init__(self, field: str, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"field": field, "message": message}
        )

# Usage
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await get_user_from_db(user_id)
    if not user:
        raise UserNotFoundException(user_id)
    return user
```

### 4. Global Exception Handlers

**Custom Exception Handler**:
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """
    Handle ValueError exceptions.
    """
    logger.error(f"ValueError: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unhandled exceptions.
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )
```

**Database Exception Handler**:
```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handle database integrity errors (unique constraints, foreign keys, etc.).
    """
    logger.error(f"Database integrity error: {str(exc)}")

    # Parse the error message to provide user-friendly feedback
    error_msg = str(exc.orig)
    if "UNIQUE constraint failed" in error_msg or "duplicate key" in error_msg:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "A record with this value already exists"}
        )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database constraint violation"}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle general SQLAlchemy errors.
    """
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Database error occurred"}
    )
```

### 5. CORS Configuration

**Basic CORS Setup**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)
```

**Production CORS Configuration**:
```python
from typing import List

class Settings(BaseSettings):
    allowed_origins: List[str] = ["https://example.com", "https://www.example.com"]
    allow_credentials: bool = True
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    allowed_headers: List[str] = ["*"]

settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
    expose_headers=["X-Total-Count", "X-Page-Count"],  # Custom headers to expose
    max_age=3600,  # Cache preflight requests for 1 hour
)
```

**Dynamic CORS Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app: FastAPI, environment: str):
    """
    Configure CORS based on environment.
    """
    if environment == "development":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    elif environment == "production":
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "https://example.com",
                "https://www.example.com"
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )
```

### 6. Authentication & Authorization

**JWT Authentication**:
```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = "your-secret-key-here"  # Use environment variable in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Login endpoint
@router.post("/login")
async def login(
    credentials: LoginCredentials,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token.
    """
    user = await get_user_by_email(db, credentials.email)
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Protected endpoint
@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information.
    """
    return current_user
```

**Role-Based Authorization**:
```python
from enum import Enum
from typing import List

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    role: UserRole = UserRole.USER

def require_roles(allowed_roles: List[UserRole]):
    """
    Dependency factory to check if user has required role.
    """
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_roles([UserRole.ADMIN]))
):
    """
    Delete a user. Only admins can perform this action.
    """
    # Implementation
    pass

@router.post("/posts/{post_id}/moderate")
async def moderate_post(
    post_id: int,
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.MODERATOR]))
):
    """
    Moderate a post. Admins and moderators can perform this action.
    """
    # Implementation
    pass
```

**Permission-Based Authorization**:
```python
from typing import Set

class Permission(str, Enum):
    READ_USERS = "read:users"
    WRITE_USERS = "write:users"
    DELETE_USERS = "delete:users"
    READ_POSTS = "read:posts"
    WRITE_POSTS = "write:posts"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    permissions: str = ""  # Comma-separated permissions

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has a specific permission."""
        user_permissions = set(self.permissions.split(","))
        return permission.value in user_permissions

def require_permissions(required_permissions: List[Permission]):
    """
    Dependency factory to check if user has required permissions.
    """
    async def permission_checker(current_user: User = Depends(get_current_user)):
        for permission in required_permissions:
            if not current_user.has_permission(permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permission: {permission.value}"
                )
        return current_user
    return permission_checker

# Usage
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_permissions([Permission.DELETE_USERS]))
):
    """
    Delete a user. Requires delete:users permission.
    """
    # Implementation
    pass
```

## Security Best Practices

### 1. Input Sanitization

**HTML Sanitization**:
```python
import bleach

class PostCreate(BaseModel):
    title: str
    content: str

    @field_validator('content')
    @classmethod
    def sanitize_content(cls, v):
        """Sanitize HTML content to prevent XSS."""
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li']
        allowed_attributes = {'a': ['href', 'title']}
        return bleach.clean(v, tags=allowed_tags, attributes=allowed_attributes)
```

**SQL Injection Prevention**:
```python
# GOOD: Using parameterized queries (SQLModel/SQLAlchemy does this automatically)
from sqlmodel import select

async def get_user_by_email(db: Session, email: str):
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalar_one_or_none()

# BAD: String concatenation (NEVER DO THIS)
# query = f"SELECT * FROM users WHERE email = '{email}'"  # VULNERABLE TO SQL INJECTION
```

### 2. Rate Limiting

**Simple Rate Limiting Middleware**:
```python
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = datetime.now()

        # Clean old requests
        self.clients[client_ip] = [
            req_time for req_time in self.clients[client_ip]
            if now - req_time < timedelta(seconds=self.period)
        ]

        # Check rate limit
        if len(self.clients[client_ip]) >= self.calls:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Rate limit exceeded"}
            )

        # Add current request
        self.clients[client_ip].append(now)

        response = await call_next(request)
        return response

# Add to app
app.add_middleware(RateLimitMiddleware, calls=100, period=60)
```

### 3. Security Headers

**Security Headers Middleware**:
```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### 4. API Key Authentication

**API Key Dependency**:
```python
from fastapi import Security
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    """
    Validate API key.
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing"
        )

    # Validate against database or environment variable
    valid_api_keys = ["your-api-key-here"]  # Load from database in production

    if api_key not in valid_api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )

    return api_key

# Usage
@router.get("/protected")
async def protected_endpoint(api_key: str = Depends(get_api_key)):
    """
    Protected endpoint requiring API key.
    """
    return {"message": "Access granted"}
```

## Testing

### Validation Testing

```python
from fastapi.testclient import TestClient

def test_user_creation_validation(client: TestClient):
    """Test user creation with invalid data."""

    # Test missing required field
    response = client.post("/api/v1/users/", json={
        "username": "testuser"
        # Missing email and password
    })
    assert response.status_code == 422

    # Test invalid email
    response = client.post("/api/v1/users/", json={
        "email": "invalid-email",
        "username": "testuser",
        "password": "Test123!"
    })
    assert response.status_code == 422

    # Test weak password
    response = client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "weak"
    })
    assert response.status_code == 422

    # Test valid data
    response = client.post("/api/v1/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "Test123!"
    })
    assert response.status_code == 201
```

### Authentication Testing

```python
def test_authentication(client: TestClient):
    """Test authentication flow."""

    # Test login with invalid credentials
    response = client.post("/api/v1/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

    # Test login with valid credentials
    response = client.post("/api/v1/login", json={
        "email": "test@example.com",
        "password": "Test123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Test accessing protected endpoint without token
    response = client.get("/api/v1/me")
    assert response.status_code == 401

    # Test accessing protected endpoint with token
    token = response.json()["access_token"]
    response = client.get(
        "/api/v1/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```

### Error Handling Testing

```python
def test_error_handling(client: TestClient):
    """Test error handling."""

    # Test 404 error
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "detail" in response.json()

    # Test validation error
    response = client.post("/api/v1/users/", json={})
    assert response.status_code == 422
    assert "errors" in response.json()
```

## Summary

This skill provides comprehensive guidance for:
- **Validation**: Pydantic models, custom validators, input validation
- **Error Handling**: HTTPException, custom exceptions, global handlers
- **Security**: Authentication, authorization, CORS, rate limiting, security headers
- **Best Practices**: Input sanitization, SQL injection prevention, API key auth
- **Testing**: Validation, authentication, and error handling tests

Use this skill to ensure your FastAPI applications are secure, reliable, and properly validated at all levels.
