# FastAPI Core & Routing

## Expertise
Expert skill for building and organizing FastAPI applications with clean architecture, proper routing, dependency injection, and integration with external skills like SQLModel. Specializes in FastAPI app initialization, APIRouter setup, async endpoints, and lifecycle management.

## Purpose
This skill handles the core FastAPI application structure and routing concerns, enabling you to:
- Initialize FastAPI applications with proper configuration
- Organize routes using APIRouter for clean separation of concerns
- Implement dependency injection patterns
- Create async endpoints with proper error handling
- Manage application lifecycle (startup/shutdown events)
- Integrate seamlessly with database skills (SQLModel, etc.)

## When to Use
Use this skill when you need to:
- Set up a new FastAPI application from scratch
- Organize routes into logical groups (users, auth, products, etc.)
- Implement dependency injection for database sessions, auth, etc.
- Create async API endpoints
- Configure application startup and shutdown logic
- Structure a FastAPI project for scalability

## Core Concepts

### 1. FastAPI App Initialization

**Basic Setup**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    """
    app = FastAPI(
        title="My API",
        description="API description",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()
```

**With Environment Configuration**:
```python
from fastapi import FastAPI
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)
```

### 2. APIRouter Setup and Route Grouping

**Router Organization**:
```python
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all users with pagination."""
    users = await user_service.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific user by ID."""
    user = await user_service.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    return await user_service.create_user(db, user=user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing user."""
    updated_user = await user_service.update_user(db, user_id=user_id, user=user)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a user."""
    success = await user_service.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
```

**Including Routers in Main App**:
```python
# main.py
from fastapi import FastAPI
from routers import users, auth, products

app = FastAPI()

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 3. Dependency Injection

**Database Session Dependency**:
```python
from typing import Generator
from sqlmodel import Session, create_engine
from fastapi import Depends

# Database setup
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Automatically closes the session after the request.
    """
    with Session(engine) as session:
        yield session
```

**Async Database Session Dependency**:
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_db() -> AsyncSession:
    """
    Async dependency that provides a database session.
    """
    async with async_session() as session:
        yield session
```

**Authentication Dependency**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that validates JWT token and returns current user.
    """
    token = credentials.credentials
    payload = decode_jwt(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user_by_id(db, user_id=payload["sub"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user

# Usage in endpoint
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user information."""
    return current_user
```

**Dependency with Configuration**:
```python
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    """
    Cached dependency that provides application settings.
    """
    return Settings()

@router.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    """Get application configuration."""
    return {"app_name": settings.app_name}
```

### 4. Async Endpoint Definitions

**Basic Async Endpoint**:
```python
@router.get("/items/{item_id}")
async def get_item(item_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Async endpoint that fetches an item from the database.
    """
    result = await db.execute(select(Item).where(Item.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
```

**Async with Multiple Operations**:
```python
@router.post("/orders")
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create an order with multiple async operations.
    """
    # Validate items exist
    items = await validate_items(db, order.item_ids)

    # Calculate total
    total = sum(item.price * order.quantities[item.id] for item in items)

    # Create order
    new_order = Order(
        user_id=current_user.id,
        total=total,
        status="pending"
    )
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    # Send notification (async)
    await send_order_notification(current_user.email, new_order.id)

    return new_order
```

**Background Tasks**:
```python
from fastapi import BackgroundTasks

def send_email_notification(email: str, message: str):
    """Background task to send email."""
    # Email sending logic
    pass

@router.post("/register")
async def register_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Register user and send welcome email in background.
    """
    new_user = await user_service.create_user(db, user=user)

    # Add background task
    background_tasks.add_task(
        send_email_notification,
        new_user.email,
        "Welcome to our platform!"
    )

    return new_user
```

### 5. App Startup and Shutdown Events

**Lifecycle Events**:
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle.
    Code before yield runs on startup.
    Code after yield runs on shutdown.
    """
    # Startup
    print("Starting up...")

    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Initialize cache
    await init_cache()

    # Start background workers
    await start_workers()

    yield

    # Shutdown
    print("Shutting down...")

    # Close database connections
    await engine.dispose()

    # Close cache connections
    await close_cache()

    # Stop background workers
    await stop_workers()

app = FastAPI(lifespan=lifespan)
```

**Legacy Event Handlers** (for older FastAPI versions):
```python
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("Application starting...")
    # Initialize resources
    await init_database()
    await init_cache()

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("Application shutting down...")
    # Cleanup resources
    await close_database()
    await close_cache()
```

## Project Structure

### Recommended Directory Layout

```
project/
├── main.py                 # FastAPI app entry point
├── core/
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── security.py        # Authentication/authorization
│   └── dependencies.py    # Shared dependencies
├── routers/
│   ├── __init__.py
│   ├── users.py           # User routes
│   ├── auth.py            # Authentication routes
│   └── products.py        # Product routes
├── schemas/
│   ├── __init__.py
│   ├── user.py            # Pydantic models for users
│   └── product.py         # Pydantic models for products
├── services/
│   ├── __init__.py
│   ├── user_service.py    # Business logic for users
│   └── product_service.py # Business logic for products
├── models/
│   ├── __init__.py
│   ├── user.py            # SQLModel database models
│   └── product.py         # SQLModel database models
└── requirements.txt
```

## Integration with SQLModel

**Complete Integration Example**:

```python
# models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str
    hashed_password: str

# schemas/user.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True

# services/user_service.py
from sqlmodel import Session, select
from models.user import User
from schemas.user import UserCreate

async def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.get(User, user_id)

# routers/users.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from core.dependencies import get_db
from services import user_service
from schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    return await user_service.create_user(db, user=user)

# main.py
from fastapi import FastAPI
from routers import users
from core.config import settings

app = FastAPI(title=settings.app_name)
app.include_router(users.router, prefix="/api/v1")
```

## Best Practices

### 1. Route Organization
- Group related endpoints in separate router files
- Use consistent naming conventions
- Add tags for API documentation grouping
- Include response models for type safety

### 2. Dependency Injection
- Use dependencies for database sessions
- Implement authentication as a dependency
- Cache expensive dependencies with `@lru_cache`
- Keep dependencies focused and reusable

### 3. Error Handling
- Use HTTPException for API errors
- Provide clear error messages
- Include appropriate status codes
- Add custom exception handlers when needed

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

### 4. Async Best Practices
- Use async endpoints for I/O operations
- Await all async calls
- Use async database drivers when possible
- Don't mix sync and async code unnecessarily

### 5. Configuration Management
- Use Pydantic Settings for configuration
- Store secrets in environment variables
- Validate configuration on startup
- Use different configs for dev/staging/prod

### 6. API Versioning
- Use URL path versioning (`/api/v1/`, `/api/v2/`)
- Maintain backward compatibility
- Document breaking changes
- Deprecate old versions gracefully

## Common Patterns

### Health Check Endpoint
```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Check application and database health."""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
```

### Pagination
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

@router.get("/items", response_model=PaginatedResponse[ItemResponse])
async def list_items(
    page: int = 1,
    size: int = 20,
    db: Session = Depends(get_db)
):
    """List items with pagination."""
    skip = (page - 1) * size
    items = await item_service.get_items(db, skip=skip, limit=size)
    total = await item_service.count_items(db)

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
```

### Request Validation
```python
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v
```

## Testing

### Test Setup
```python
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

# Test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Test example
def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser", "password": "Test123!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```

## Summary

This skill provides comprehensive guidance for building FastAPI applications with:
- Clean architecture and separation of concerns
- Proper routing and dependency injection
- Async endpoint patterns
- Lifecycle management
- Integration with SQLModel and other skills
- Production-ready best practices

Use this skill as your foundation for all FastAPI application development, ensuring consistency, maintainability, and scalability across your projects.
