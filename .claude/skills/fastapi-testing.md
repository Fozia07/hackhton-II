# FastAPI Testing

## Expertise
Expert skill for testing FastAPI applications with comprehensive patterns for unit tests, integration tests, and end-to-end tests. Specializes in TestClient usage, pytest fixtures, database testing, authentication testing, and mocking strategies.

## Purpose
This skill handles testing concerns for FastAPI applications, enabling you to:
- Write comprehensive tests for API endpoints
- Test authentication and authorization flows
- Test database operations with isolated test databases
- Mock external dependencies and services
- Test validation and error handling
- Implement integration and end-to-end tests
- Measure test coverage
- Test async endpoints and background tasks

## When to Use
Use this skill when you need to:
- Set up testing infrastructure for FastAPI applications
- Write unit tests for individual endpoints
- Test CRUD operations with database isolation
- Test authentication and authorization logic
- Test validation rules and error responses
- Mock external API calls and services
- Implement integration tests across multiple endpoints
- Test configuration and dependency injection
- Measure and improve test coverage

## Core Concepts

### 1. TestClient Setup

**Basic TestClient Usage**:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API"}

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
```

**TestClient with Context Manager**:
```python
def test_with_context_manager():
    """Test using context manager for proper cleanup."""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
```

### 2. Pytest Fixtures

**Basic Fixtures**:
```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from core.config import Settings, get_settings
from core.dependencies import get_db

# Test database fixture
@pytest.fixture(name="session")
def session_fixture():
    """
    Create a test database session.
    Uses in-memory SQLite for fast, isolated tests.
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Test settings fixture
@pytest.fixture(name="test_settings")
def test_settings_fixture():
    """Provide test settings."""
    return Settings(
        app_name="Test App",
        environment="testing",
        debug=True,
        log_level="DEBUG",
        database_url="sqlite://",
        secret_key="test-secret-key-min-32-chars-long",
        jwt_secret="test-jwt-secret-min-32-chars-long"
    )

# Test client fixture
@pytest.fixture(name="client")
def client_fixture(session: Session, test_settings: Settings):
    """
    Create a test client with overridden dependencies.
    """
    def get_session_override():
        return session

    def get_settings_override():
        return test_settings

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[get_settings] = get_settings_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
```

**Advanced Fixtures with Async Support**:
```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

@pytest_asyncio.fixture
async def async_session():
    """
    Create async test database session.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False}
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()
```

**Fixture Scopes**:
```python
# Function scope (default) - runs for each test
@pytest.fixture(scope="function")
def function_scoped_fixture():
    """Runs before each test function."""
    return "function"

# Module scope - runs once per test module
@pytest.fixture(scope="module")
def module_scoped_fixture():
    """Runs once per test file."""
    return "module"

# Session scope - runs once per test session
@pytest.fixture(scope="session")
def session_scoped_fixture():
    """Runs once for entire test session."""
    return "session"
```

### 3. Testing CRUD Operations

**Testing Create Operations**:
```python
def test_create_user(client: TestClient):
    """Test user creation."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "password" not in data  # Password should not be returned

def test_create_user_duplicate_email(client: TestClient):
    """Test creating user with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "Test123!@#"
    }

    # Create first user
    response1 = client.post("/api/v1/users/", json=user_data)
    assert response1.status_code == 201

    # Try to create duplicate
    user_data["username"] = "user2"  # Different username, same email
    response2 = client.post("/api/v1/users/", json=user_data)
    assert response2.status_code == 400
    assert "already exists" in response2.json()["detail"].lower()
```

**Testing Read Operations**:
```python
def test_get_user(client: TestClient, session: Session):
    """Test getting a user by ID."""
    # Create user directly in database
    user = User(email="test@example.com", username="testuser", hashed_password="hashed")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Get user via API
    response = client.get(f"/api/v1/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == user.email

def test_get_user_not_found(client: TestClient):
    """Test getting non-existent user returns 404."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_list_users(client: TestClient, session: Session):
    """Test listing users with pagination."""
    # Create multiple users
    for i in range(5):
        user = User(
            email=f"user{i}@example.com",
            username=f"user{i}",
            hashed_password="hashed"
        )
        session.add(user)
    session.commit()

    # List users
    response = client.get("/api/v1/users/?skip=0&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
```

**Testing Update Operations**:
```python
def test_update_user(client: TestClient, session: Session):
    """Test updating a user."""
    # Create user
    user = User(email="test@example.com", username="oldname", hashed_password="hashed")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Update user
    response = client.put(
        f"/api/v1/users/{user.id}",
        json={"username": "newname"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newname"
    assert data["email"] == "test@example.com"  # Email unchanged

def test_update_user_not_found(client: TestClient):
    """Test updating non-existent user returns 404."""
    response = client.put(
        "/api/v1/users/99999",
        json={"username": "newname"}
    )
    assert response.status_code == 404
```

**Testing Delete Operations**:
```python
def test_delete_user(client: TestClient, session: Session):
    """Test deleting a user."""
    # Create user
    user = User(email="test@example.com", username="testuser", hashed_password="hashed")
    session.add(user)
    session.commit()
    session.refresh(user)
    user_id = user.id

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404

def test_delete_user_not_found(client: TestClient):
    """Test deleting non-existent user returns 404."""
    response = client.delete("/api/v1/users/99999")
    assert response.status_code == 404
```

### 4. Testing Authentication and Authorization

**Authentication Fixtures**:
```python
import pytest
from datetime import datetime, timedelta
from jose import jwt

@pytest.fixture
def test_user(session: Session):
    """Create a test user."""
    user = User(
        email="testuser@example.com",
        username="testuser",
        hashed_password=hash_password("Test123!@#"),
        role="user"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def admin_user(session: Session):
    """Create an admin user."""
    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=hash_password("Admin123!@#"),
        role="admin"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def auth_token(test_user: User, test_settings: Settings):
    """Generate authentication token for test user."""
    payload = {
        "sub": str(test_user.id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, test_settings.jwt_secret, algorithm=test_settings.jwt_algorithm)
    return token

@pytest.fixture
def admin_token(admin_user: User, test_settings: Settings):
    """Generate authentication token for admin user."""
    payload = {
        "sub": str(admin_user.id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    token = jwt.encode(payload, test_settings.jwt_secret, algorithm=test_settings.jwt_algorithm)
    return token
```

**Testing Login**:
```python
def test_login_success(client: TestClient, test_user: User):
    """Test successful login."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user: User):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "WrongPassword"
        }
    )
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()

def test_login_user_not_found(client: TestClient):
    """Test login with non-existent user."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 401
```

**Testing Protected Endpoints**:
```python
def test_protected_endpoint_without_token(client: TestClient):
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower()

def test_protected_endpoint_with_token(client: TestClient, auth_token: str):
    """Test accessing protected endpoint with valid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"

def test_protected_endpoint_with_invalid_token(client: TestClient):
    """Test accessing protected endpoint with invalid token."""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401

def test_protected_endpoint_with_expired_token(client: TestClient, test_user: User, test_settings: Settings):
    """Test accessing protected endpoint with expired token."""
    # Create expired token
    payload = {
        "sub": str(test_user.id),
        "exp": datetime.utcnow() - timedelta(minutes=30)  # Expired
    }
    expired_token = jwt.encode(payload, test_settings.jwt_secret, algorithm=test_settings.jwt_algorithm)

    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
```

**Testing Role-Based Authorization**:
```python
def test_admin_endpoint_as_user(client: TestClient, auth_token: str):
    """Test accessing admin endpoint as regular user."""
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

def test_admin_endpoint_as_admin(client: TestClient, admin_token: str):
    """Test accessing admin endpoint as admin."""
    response = client.get(
        "/api/v1/admin/users",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
```

### 5. Testing Validation and Error Handling

**Testing Request Validation**:
```python
def test_create_user_invalid_email(client: TestClient):
    """Test creating user with invalid email."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "not-an-email",
            "username": "testuser",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("email" in str(error).lower() for error in errors)

def test_create_user_weak_password(client: TestClient):
    """Test creating user with weak password."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "weak"
        }
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("password" in str(error).lower() for error in errors)

def test_create_user_missing_fields(client: TestClient):
    """Test creating user with missing required fields."""
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com"}  # Missing username and password
    )
    assert response.status_code == 422
```

**Testing Query Parameter Validation**:
```python
def test_list_users_invalid_pagination(client: TestClient):
    """Test listing users with invalid pagination parameters."""
    response = client.get("/api/v1/users/?skip=-1&limit=0")
    assert response.status_code == 422

def test_list_users_limit_too_high(client: TestClient):
    """Test listing users with limit exceeding maximum."""
    response = client.get("/api/v1/users/?limit=1000")
    assert response.status_code == 422
```

**Testing Custom Error Responses**:
```python
def test_custom_business_logic_error(client: TestClient, test_user: User, auth_token: str):
    """Test custom business logic error."""
    # Try to perform action that violates business rules
    response = client.post(
        "/api/v1/orders/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={"items": []}  # Empty order not allowed
    )
    assert response.status_code == 400
    assert "cannot create empty order" in response.json()["detail"].lower()
```

### 6. Mocking External Dependencies

**Mocking External API Calls**:
```python
from unittest.mock import Mock, patch
import pytest

@pytest.fixture
def mock_external_api():
    """Mock external API calls."""
    with patch("services.external_service.call_external_api") as mock:
        mock.return_value = {"status": "success", "data": "mocked"}
        yield mock

def test_endpoint_with_external_api(client: TestClient, mock_external_api: Mock):
    """Test endpoint that calls external API."""
    response = client.get("/api/v1/external-data")
    assert response.status_code == 200
    assert response.json()["data"] == "mocked"
    mock_external_api.assert_called_once()

def test_endpoint_external_api_failure(client: TestClient):
    """Test endpoint when external API fails."""
    with patch("services.external_service.call_external_api") as mock:
        mock.side_effect = Exception("External API error")

        response = client.get("/api/v1/external-data")
        assert response.status_code == 503
        assert "external service unavailable" in response.json()["detail"].lower()
```

**Mocking Email Service**:
```python
@pytest.fixture
def mock_email_service():
    """Mock email sending."""
    with patch("services.email_service.send_email") as mock:
        yield mock

def test_user_registration_sends_email(client: TestClient, mock_email_service: Mock):
    """Test that user registration sends welcome email."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 201
    mock_email_service.assert_called_once_with(
        to="test@example.com",
        subject="Welcome!",
        body=pytest.approx(str, rel=1e-2)  # Any string
    )
```

**Mocking Redis Cache**:
```python
@pytest.fixture
def mock_redis():
    """Mock Redis cache."""
    with patch("services.cache_service.redis_client") as mock:
        mock.get.return_value = None
        mock.set.return_value = True
        yield mock

def test_endpoint_with_cache(client: TestClient, mock_redis: Mock):
    """Test endpoint that uses caching."""
    response = client.get("/api/v1/cached-data")
    assert response.status_code == 200
    mock_redis.get.assert_called_once()
    mock_redis.set.assert_called_once()
```

### 7. Integration Testing

**Testing Multiple Endpoints Together**:
```python
def test_user_workflow(client: TestClient):
    """Test complete user workflow: register, login, get profile, update, delete."""
    # 1. Register
    register_response = client.post(
        "/api/v1/users/",
        json={
            "email": "workflow@example.com",
            "username": "workflowuser",
            "password": "Test123!@#"
        }
    )
    assert register_response.status_code == 201
    user_id = register_response.json()["id"]

    # 2. Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "workflow@example.com",
            "password": "Test123!@#"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get profile
    profile_response = client.get("/api/v1/users/me", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["email"] == "workflow@example.com"

    # 4. Update profile
    update_response = client.put(
        f"/api/v1/users/{user_id}",
        headers=headers,
        json={"username": "updateduser"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["username"] == "updateduser"

    # 5. Delete account
    delete_response = client.delete(f"/api/v1/users/{user_id}", headers=headers)
    assert delete_response.status_code == 204

    # 6. Verify deletion
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 404
```

**Testing Relationships and Foreign Keys**:
```python
def test_user_posts_relationship(client: TestClient, auth_token: str, test_user: User):
    """Test creating posts for a user and retrieving them."""
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Create posts
    for i in range(3):
        response = client.post(
            "/api/v1/posts/",
            headers=headers,
            json={"title": f"Post {i}", "content": f"Content {i}"}
        )
        assert response.status_code == 201

    # Get user's posts
    response = client.get(f"/api/v1/users/{test_user.id}/posts", headers=headers)
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 3
```

### 8. Testing Async Endpoints

**Testing Async Operations**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    """Test async endpoint."""
    response = await async_client.get("/api/v1/async-data")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_database_operation(async_session: AsyncSession):
    """Test async database operation."""
    user = User(email="async@example.com", username="asyncuser", hashed_password="hashed")
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.id is not None
```

### 9. Testing Background Tasks

**Testing Background Task Execution**:
```python
from unittest.mock import Mock, patch

def test_background_task_triggered(client: TestClient):
    """Test that background task is triggered."""
    with patch("services.background_tasks.process_data") as mock_task:
        response = client.post(
            "/api/v1/process",
            json={"data": "test"}
        )
        assert response.status_code == 202
        mock_task.assert_called_once()
```

## Testing Best Practices

### 1. Test Organization
- Group related tests in classes
- Use descriptive test names (test_what_when_expected)
- One assertion per test when possible
- Test happy path and error cases

### 2. Test Isolation
- Each test should be independent
- Use fixtures for setup and teardown
- Don't rely on test execution order
- Clean up resources after tests

### 3. Test Coverage
- Aim for 80%+ code coverage
- Test all error paths
- Test edge cases and boundary conditions
- Test validation rules

### 4. Test Data
- Use factories or fixtures for test data
- Don't use production data in tests
- Use realistic but safe test data
- Clean up test data after tests

### 5. Mocking Strategy
- Mock external dependencies (APIs, email, etc.)
- Don't mock what you own
- Mock at the boundary
- Verify mock calls when important

## Running Tests

**Basic pytest Commands**:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_create_user

# Run tests matching pattern
pytest -k "test_create"

# Run with verbose output
pytest -v

# Run with print statements
pytest -s

# Stop on first failure
pytest -x

# Run in parallel
pytest -n auto
```

**pytest.ini Configuration**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

## Summary

This skill provides comprehensive guidance for testing FastAPI applications with:
- TestClient setup and usage patterns
- Pytest fixtures for database, settings, and authentication
- CRUD operation testing patterns
- Authentication and authorization testing
- Validation and error handling tests
- Mocking strategies for external dependencies
- Integration testing patterns
- Async endpoint testing
- Background task testing
- Best practices for test organization and coverage

Use this skill to ensure your FastAPI applications are thoroughly tested, reliable, and maintainable with comprehensive test coverage across all layers.
