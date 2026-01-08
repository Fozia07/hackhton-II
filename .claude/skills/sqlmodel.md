# SQLModel Expert

## Expertise
Comprehensive guidance for using SQLModel - a library that combines SQLAlchemy and Pydantic for database operations in Python. This skill provides practical patterns for defining models, managing connections, performing CRUD operations, and integrating with FastAPI.

## Purpose
This skill helps developers effectively work with SQL databases using SQLModel's powerful combination of SQLAlchemy's database capabilities and Pydantic's data validation. It covers the complete lifecycle from model definition to production deployment.

## When to Use
Use this skill when you need to:
- Define database models with type hints and validation
- Set up database connections and manage sessions
- Perform CRUD operations (Create, Read, Update, Delete)
- Query data with filters, joins, and relationships
- Handle database migrations and schema changes
- Integrate SQLModel with FastAPI applications
- Implement best practices for database operations
- Handle errors and validate data effectively

## Core Concepts

### 1. Model Definition
SQLModel combines SQLAlchemy's ORM with Pydantic's validation:

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    """User model with validation and database mapping."""
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True, regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    posts: list["Post"] = Relationship(back_populates="author")

class Post(SQLModel, table=True):
    """Post model with foreign key relationship."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    content: str
    published: bool = Field(default=False)
    author_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: Optional[User] = Relationship(back_populates="posts")
```

**Key Points:**
- `table=True` marks the class as a database table
- `Field()` provides validation and database constraints
- `Optional[int]` with `primary_key=True` for auto-increment IDs
- `Relationship()` defines ORM relationships
- Type hints enable both validation and IDE support

### 2. Database Connection and Session Management

```python
from sqlmodel import create_engine, Session, SQLModel
from contextlib import contextmanager
from typing import Generator

# Database URL patterns:
# SQLite: "sqlite:///database.db"
# PostgreSQL: "postgresql://user:password@localhost/dbname"
# MySQL: "mysql://user:password@localhost/dbname"

DATABASE_URL = "sqlite:///./app.db"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    connect_args={"check_same_thread": False}  # SQLite specific
)

def create_db_and_tables():
    """Create all tables defined in SQLModel metadata."""
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Alternative: Dependency injection for FastAPI
def get_db_session():
    """FastAPI dependency for database sessions."""
    with Session(engine) as session:
        yield session
```

**Best Practices:**
- Use connection pooling for production databases
- Always use context managers or try-finally for sessions
- Disable `echo=True` in production
- Configure appropriate pool sizes for your workload

### 3. CRUD Operations

#### Create (Insert)
```python
from sqlmodel import Session, select

def create_user(session: Session, username: str, email: str, full_name: str = None) -> User:
    """Create a new user with validation."""
    user = User(username=username, email=email, full_name=full_name)
    session.add(user)
    session.commit()
    session.refresh(user)  # Get the generated ID
    return user

# Bulk insert
def create_users_bulk(session: Session, users_data: list[dict]) -> list[User]:
    """Create multiple users efficiently."""
    users = [User(**data) for data in users_data]
    session.add_all(users)
    session.commit()
    for user in users:
        session.refresh(user)
    return users
```

#### Read (Query)
```python
def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return session.get(User, user_id)

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Get user by username with error handling."""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_active_users(session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get paginated list of active users."""
    statement = select(User).where(User.is_active == True).offset(skip).limit(limit)
    return session.exec(statement).all()

def search_users(session: Session, search_term: str) -> list[User]:
    """Search users by username or email."""
    statement = select(User).where(
        (User.username.contains(search_term)) |
        (User.email.contains(search_term))
    )
    return session.exec(statement).all()
```

#### Update
```python
def update_user(session: Session, user_id: int, **kwargs) -> Optional[User]:
    """Update user fields dynamically."""
    user = session.get(User, user_id)
    if not user:
        return None

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def deactivate_user(session: Session, user_id: int) -> bool:
    """Soft delete by deactivating user."""
    user = session.get(User, user_id)
    if not user:
        return False

    user.is_active = False
    session.add(user)
    session.commit()
    return True
```

#### Delete
```python
def delete_user(session: Session, user_id: int) -> bool:
    """Hard delete a user."""
    user = session.get(User, user_id)
    if not user:
        return False

    session.delete(user)
    session.commit()
    return True

def delete_inactive_users(session: Session) -> int:
    """Bulk delete inactive users."""
    statement = select(User).where(User.is_active == False)
    users = session.exec(statement).all()
    count = len(users)

    for user in users:
        session.delete(user)

    session.commit()
    return count
```

### 4. Advanced Querying and Relationships

```python
from sqlmodel import select, col

def get_user_with_posts(session: Session, user_id: int) -> Optional[User]:
    """Get user with all their posts (eager loading)."""
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    if user:
        # Access posts - SQLModel handles the relationship
        _ = user.posts  # This triggers loading if not already loaded
    return user

def get_published_posts_with_authors(session: Session) -> list[Post]:
    """Get all published posts with author information."""
    statement = select(Post).where(Post.published == True)
    posts = session.exec(statement).all()
    # Authors are loaded automatically when accessed
    return posts

def get_users_with_post_count(session: Session):
    """Complex query with aggregation."""
    from sqlalchemy import func

    statement = (
        select(User, func.count(Post.id).label("post_count"))
        .join(Post, isouter=True)
        .group_by(User.id)
    )
    results = session.exec(statement).all()
    return results

def filter_posts_by_date_range(
    session: Session,
    start_date: datetime,
    end_date: datetime
) -> list[Post]:
    """Filter posts by date range."""
    statement = select(Post).where(
        Post.created_at >= start_date,
        Post.created_at <= end_date
    )
    return session.exec(statement).all()
```

### 5. FastAPI Integration

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

app = FastAPI()

# Dependency
def get_session():
    with Session(engine) as session:
        yield session

# Pydantic models for API (separate from database models)
class UserCreate(SQLModel):
    """Schema for creating users (no ID)."""
    username: str = Field(min_length=3, max_length=50)
    email: str
    full_name: Optional[str] = None

class UserRead(SQLModel):
    """Schema for reading users (includes ID)."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

class UserUpdate(SQLModel):
    """Schema for updating users (all fields optional)."""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

# API Endpoints
@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: UserCreate, session: Session = Depends(get_session)):
    """Create a new user."""
    # Check if username exists
    existing = session.exec(select(User).where(User.username == user.username)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """List all users with pagination."""
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.patch("/users/{user_id}", response_model=UserRead)
def update_user_endpoint(
    user_id: int,
    user_update: UserUpdate,
    session: Session = Depends(get_session)
):
    """Update a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, session: Session = Depends(get_session)):
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    session.delete(user)
    session.commit()
    return None

@app.on_event("startup")
def on_startup():
    """Create tables on application startup."""
    create_db_and_tables()
```

### 6. Database Migrations with Alembic

```python
# Install: pip install alembic

# Initialize Alembic
# alembic init alembic

# alembic/env.py configuration
from sqlmodel import SQLModel
from app.models import User, Post  # Import all models

target_metadata = SQLModel.metadata

# Generate migration
# alembic revision --autogenerate -m "Add user and post tables"

# Apply migration
# alembic upgrade head

# Rollback migration
# alembic downgrade -1
```

**Migration Best Practices:**
- Always review auto-generated migrations
- Test migrations on a copy of production data
- Create separate migrations for data changes
- Keep migrations small and focused
- Document breaking changes

### 7. Error Handling and Validation

```python
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError

def safe_create_user(session: Session, user_data: dict) -> tuple[Optional[User], Optional[str]]:
    """Create user with comprehensive error handling."""
    try:
        # Pydantic validation
        user = User(**user_data)

        # Database operation
        session.add(user)
        session.commit()
        session.refresh(user)
        return user, None

    except ValidationError as e:
        return None, f"Validation error: {e.errors()}"

    except IntegrityError as e:
        session.rollback()
        if "UNIQUE constraint" in str(e):
            return None, "Username or email already exists"
        return None, f"Database integrity error: {str(e)}"

    except SQLAlchemyError as e:
        session.rollback()
        return None, f"Database error: {str(e)}"

    except Exception as e:
        session.rollback()
        return None, f"Unexpected error: {str(e)}"

def safe_query_with_retry(session: Session, statement, max_retries: int = 3):
    """Execute query with retry logic for transient failures."""
    import time

    for attempt in range(max_retries):
        try:
            return session.exec(statement).all()
        except SQLAlchemyError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
            session.rollback()
```

### 8. Testing Patterns

```python
import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

def test_create_user(session: Session):
    """Test user creation."""
    user = User(username="testuser", email="test@example.com")
    session.add(user)
    session.commit()

    assert user.id is not None
    assert user.username == "testuser"
    assert user.is_active is True

def test_user_validation():
    """Test Pydantic validation."""
    with pytest.raises(ValidationError):
        User(username="ab", email="invalid-email")  # Too short username

def test_unique_constraint(session: Session):
    """Test unique constraint enforcement."""
    user1 = User(username="testuser", email="test1@example.com")
    user2 = User(username="testuser", email="test2@example.com")

    session.add(user1)
    session.commit()

    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()
```

### 9. Async/Await Support

SQLModel supports asynchronous operations for high-performance applications. This is essential for modern Python web frameworks and concurrent workloads.

#### Async Engine and Session Setup

```python
from sqlmodel import SQLModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

# Async database URL (note the async driver)
# PostgreSQL: "postgresql+asyncpg://user:password@localhost/dbname"
# SQLite: "sqlite+aiosqlite:///./app.db"
ASYNC_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# Create async engine
async_engine: AsyncEngine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # Disable in production
    future=True,
    pool_size=20,
    max_overflow=10
)

# Create async session factory
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def create_db_and_tables_async():
    """Create all tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async session dependency for FastAPI."""
    async with async_session_maker() as session:
        yield session
```

#### Async CRUD Operations

```python
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_user_async(session: AsyncSession, username: str, email: str) -> User:
    """Create a user asynchronously."""
    user = User(username=username, email=email)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def get_user_by_id_async(session: AsyncSession, user_id: int) -> Optional[User]:
    """Get user by ID asynchronously."""
    return await session.get(User, user_id)

async def get_users_async(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> list[User]:
    """Get paginated users asynchronously."""
    statement = select(User).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()

async def search_users_async(session: AsyncSession, search_term: str) -> list[User]:
    """Search users asynchronously."""
    statement = select(User).where(
        (User.username.contains(search_term)) |
        (User.email.contains(search_term))
    )
    result = await session.exec(statement)
    return result.all()

async def update_user_async(
    session: AsyncSession,
    user_id: int,
    **kwargs
) -> Optional[User]:
    """Update user asynchronously."""
    user = await session.get(User, user_id)
    if not user:
        return None

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user_async(session: AsyncSession, user_id: int) -> bool:
    """Delete user asynchronously."""
    user = await session.get(User, user_id)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True
```

#### Async Relationships and Complex Queries

```python
from sqlalchemy import func
from sqlalchemy.orm import selectinload

async def get_user_with_posts_async(
    session: AsyncSession,
    user_id: int
) -> Optional[User]:
    """Get user with posts using eager loading."""
    statement = (
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    result = await session.exec(statement)
    return result.first()

async def get_users_with_post_count_async(session: AsyncSession):
    """Get users with post count asynchronously."""
    statement = (
        select(User, func.count(Post.id).label("post_count"))
        .join(Post, isouter=True)
        .group_by(User.id)
    )
    result = await session.exec(statement)
    return result.all()

async def bulk_create_users_async(
    session: AsyncSession,
    users_data: list[dict]
) -> list[User]:
    """Bulk create users asynchronously."""
    users = [User(**data) for data in users_data]
    session.add_all(users)
    await session.commit()

    # Refresh all users to get generated IDs
    for user in users:
        await session.refresh(user)

    return users
```

#### Async FastAPI Integration

```python
from fastapi import FastAPI, Depends, HTTPException, status
from typing import List

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    """Initialize database on startup."""
    await create_db_and_tables_async()

@app.on_event("shutdown")
async def on_shutdown():
    """Cleanup on shutdown."""
    await async_engine.dispose()

# Async endpoints
@app.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new user asynchronously."""
    # Check if username exists
    statement = select(User).where(User.username == user.username)
    result = await session.exec(statement)
    existing = result.first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    db_user = User.model_validate(user)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserRead])
async def list_users_endpoint(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    """List users asynchronously."""
    statement = select(User).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()

@app.get("/users/{user_id}", response_model=UserRead)
async def get_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get user by ID asynchronously."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.get("/users/{user_id}/posts", response_model=List[PostRead])
async def get_user_posts_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get all posts for a user asynchronously."""
    user = await get_user_with_posts_async(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.posts

@app.patch("/users/{user_id}", response_model=UserRead)
async def update_user_endpoint(
    user_id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Update user asynchronously."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete user asynchronously."""
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await session.delete(user)
    await session.commit()
    return None
```

#### Async Error Handling

```python
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError

async def safe_create_user_async(
    session: AsyncSession,
    user_data: dict
) -> tuple[Optional[User], Optional[str]]:
    """Create user with comprehensive async error handling."""
    try:
        user = User(**user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user, None

    except ValidationError as e:
        return None, f"Validation error: {e.errors()}"

    except IntegrityError as e:
        await session.rollback()
        if "UNIQUE constraint" in str(e):
            return None, "Username or email already exists"
        return None, f"Database integrity error: {str(e)}"

    except SQLAlchemyError as e:
        await session.rollback()
        return None, f"Database error: {str(e)}"

    except Exception as e:
        await session.rollback()
        return None, f"Unexpected error: {str(e)}"

async def safe_query_with_retry_async(
    session: AsyncSession,
    statement,
    max_retries: int = 3
):
    """Execute async query with retry logic."""
    import asyncio

    for attempt in range(max_retries):
        try:
            result = await session.exec(statement)
            return result.all()
        except SQLAlchemyError as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
            await session.rollback()
```

#### Async Testing

```python
import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

@pytest_asyncio.fixture
async def async_session():
    """Create async test database session."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=True,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_maker = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session

    await engine.dispose()

@pytest.mark.asyncio
async def test_create_user_async(async_session: AsyncSession):
    """Test async user creation."""
    user = User(username="testuser", email="test@example.com")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.id is not None
    assert user.username == "testuser"

@pytest.mark.asyncio
async def test_get_user_async(async_session: AsyncSession):
    """Test async user retrieval."""
    user = User(username="testuser", email="test@example.com")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    retrieved = await async_session.get(User, user.id)
    assert retrieved is not None
    assert retrieved.username == "testuser"

@pytest.mark.asyncio
async def test_query_users_async(async_session: AsyncSession):
    """Test async user querying."""
    users = [
        User(username=f"user{i}", email=f"user{i}@example.com")
        for i in range(5)
    ]
    async_session.add_all(users)
    await async_session.commit()

    statement = select(User)
    result = await async_session.exec(statement)
    all_users = result.all()

    assert len(all_users) == 5
```

#### Async Best Practices

**Installation:**
```bash
# For PostgreSQL
pip install sqlmodel asyncpg

# For SQLite
pip install sqlmodel aiosqlite

# For testing
pip install pytest pytest-asyncio
```

**Key Considerations:**

1. **Use Async Drivers**: Always use async database drivers (asyncpg, aiosqlite, aiomysql)
2. **Connection Pooling**: Configure appropriate pool sizes for concurrent workloads
3. **Eager Loading**: Use `selectinload()` or `joinedload()` to avoid N+1 queries
4. **Session Management**: Always use async context managers for sessions
5. **Error Handling**: Implement proper rollback logic in exception handlers
6. **Testing**: Use `pytest-asyncio` for async test support
7. **Performance**: Async operations shine with I/O-bound workloads and high concurrency
8. **Compatibility**: Not all SQLAlchemy features work identically in async mode

**When to Use Async:**
- High-concurrency web applications (FastAPI, Starlette)
- I/O-bound database operations
- Applications with many concurrent database connections
- Real-time applications requiring non-blocking operations

**When to Use Sync:**
- Simple scripts and CLI tools
- Low-concurrency applications
- Batch processing jobs
- When async complexity isn't justified by performance gains

## Best Practices Summary

### Performance
1. Use `select()` instead of `query()` for better type hints
2. Implement pagination for large datasets
3. Use eager loading for relationships when needed
4. Create appropriate indexes on frequently queried columns
5. Use connection pooling in production

### Security
1. Never concatenate user input into SQL queries (SQLModel prevents this)
2. Use parameterized queries (automatic with SQLModel)
3. Validate all input data with Pydantic
4. Store sensitive data encrypted
5. Use environment variables for database credentials

### Code Organization
1. Separate database models from API schemas
2. Use dependency injection for sessions
3. Create repository pattern for complex queries
4. Keep business logic separate from database operations
5. Use type hints consistently

### Error Handling
1. Always use try-except for database operations
2. Rollback transactions on errors
3. Provide meaningful error messages
4. Log errors for debugging
5. Handle constraint violations gracefully

### Testing
1. Use in-memory SQLite for tests
2. Create fixtures for common test data
3. Test validation rules
4. Test constraint enforcement
5. Test relationship loading

## Common Patterns

### Repository Pattern
```python
class UserRepository:
    """Repository for user operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        statement = select(User).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.session.delete(user)
        self.session.commit()
```

### Unit of Work Pattern
```python
class UnitOfWork:
    """Manage database transactions."""

    def __init__(self, session: Session):
        self.session = session
        self.users = UserRepository(session)
        self.posts = PostRepository(session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
```

## Limitations and Considerations

1. **SQLModel is built on SQLAlchemy**: Understanding SQLAlchemy concepts helps with advanced usage
2. **Async support**: Use `sqlmodel.ext.asyncio` for async operations
3. **Complex queries**: May need to drop down to SQLAlchemy for very complex queries
4. **Migration tools**: Alembic is recommended for production migrations
5. **Performance**: Profile queries and add indexes as needed

## Additional Resources

- Official Documentation: https://sqlmodel.tiangolo.com/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- FastAPI Integration: https://sqlmodel.tiangolo.com/tutorial/fastapi/
- Pydantic Validation: https://docs.pydantic.dev/

## Quick Reference

```python
# Installation
pip install sqlmodel

# Basic model
class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

# Create engine and tables
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

# Session operations
with Session(engine) as session:
    item = Item(name="Example")
    session.add(item)
    session.commit()

    # Query
    statement = select(Item).where(Item.name == "Example")
    results = session.exec(statement).all()
```
