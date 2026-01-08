# FastAPI Configuration & Logging

## Expertise
Expert skill for managing application configuration and logging in FastAPI applications with production-safe patterns. Specializes in environment-based configuration, Pydantic settings validation, structured logging, and observability best practices.

## Purpose
This skill handles configuration management and logging concerns, enabling you to:
- Manage environment-specific configuration safely
- Validate configuration at startup with Pydantic
- Inject configuration as dependencies
- Implement structured logging for production observability
- Track requests with correlation IDs
- Log application lifecycle events
- Configure logging levels and formats per environment

## When to Use
Use this skill when you need to:
- Set up environment-based configuration (.env files)
- Validate configuration with type safety
- Implement structured logging for production
- Add request tracking and correlation IDs
- Configure different logging levels for dev/staging/prod
- Log startup and shutdown events
- Integrate logging with monitoring systems
- Manage secrets and sensitive configuration

## Core Concepts

### 1. Environment Variables and .env Files

**Basic .env File Structure**:
```bash
# .env
APP_NAME="My FastAPI App"
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
DATABASE_POOL_SIZE=10

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

# CORS
CORS_ORIGINS=["https://example.com","https://app.example.com"]

# External Services
REDIS_URL=redis://localhost:6379/0
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# Feature Flags
ENABLE_REGISTRATION=true
ENABLE_EMAIL_VERIFICATION=true
```

**Development .env.example**:
```bash
# .env.example (commit this to git)
APP_NAME="My FastAPI App"
DEBUG=true
ENVIRONMENT=development
LOG_LEVEL=DEBUG

DATABASE_URL=postgresql://user:pass@localhost:5432/mydb_dev
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET=dev-jwt-secret-change-in-production

# Add all required variables with safe defaults or placeholders
```

### 2. Pydantic BaseSettings Configuration

**Basic Settings Class**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import List, Optional
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Validates configuration at startup.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra env vars
    )

    # Application
    app_name: str = Field(default="FastAPI App", description="Application name")
    debug: bool = Field(default=False, description="Debug mode")
    environment: str = Field(default="production", description="Environment (dev/staging/prod)")
    log_level: str = Field(default="INFO", description="Logging level")

    # API
    api_v1_prefix: str = Field(default="/api/v1", description="API v1 prefix")

    # Database
    database_url: str = Field(..., description="Database connection URL")
    database_pool_size: int = Field(default=10, ge=1, le=100)
    database_echo: bool = Field(default=False, description="Echo SQL queries")

    # Security
    secret_key: str = Field(..., min_length=32, description="Secret key for signing")
    jwt_secret: str = Field(..., min_length=32, description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_minutes: int = Field(default=30, ge=1)

    # CORS
    cors_origins: List[str] = Field(default=["*"], description="Allowed CORS origins")

    # Redis
    redis_url: Optional[str] = Field(default=None, description="Redis connection URL")

    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = Field(default=587)
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None

    # Feature Flags
    enable_registration: bool = Field(default=True)
    enable_email_verification: bool = Field(default=False)

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is valid."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v_upper

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment is valid."""
        valid_envs = ["development", "staging", "production"]
        v_lower = v.lower()
        if v_lower not in valid_envs:
            raise ValueError(f"Environment must be one of {valid_envs}")
        return v_lower

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "sqlite://", "mysql://")):
            raise ValueError("Database URL must start with postgresql://, sqlite://, or mysql://")
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Settings are loaded once and cached for the application lifetime.
    """
    return Settings()
```

**Advanced Settings with Nested Configuration**:
```python
from pydantic import BaseModel

class DatabaseSettings(BaseModel):
    """Database-specific settings."""
    url: str
    pool_size: int = 10
    pool_recycle: int = 3600
    echo: bool = False
    pool_pre_ping: bool = True

class RedisSettings(BaseModel):
    """Redis-specific settings."""
    url: str
    max_connections: int = 10
    decode_responses: bool = True

class LoggingSettings(BaseModel):
    """Logging-specific settings."""
    level: str = "INFO"
    format: str = "json"  # json or text
    include_request_id: bool = True

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__"  # Use DB__URL for nested config
    )

    app_name: str = "FastAPI App"
    environment: str = "production"

    # Nested configurations
    database: DatabaseSettings
    redis: Optional[RedisSettings] = None
    logging: LoggingSettings = LoggingSettings()

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment with validation."""
        try:
            return cls()
        except Exception as e:
            print(f"Configuration error: {e}")
            raise

# Usage with nested env vars:
# DB__URL=postgresql://...
# DB__POOL_SIZE=20
# LOGGING__LEVEL=DEBUG
```

### 3. Configuration Dependency Injection

**Settings Dependency**:
```python
from fastapi import Depends
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    """Cached settings dependency."""
    return Settings()

# Usage in endpoints
@router.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    """Get application configuration (safe subset)."""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
        "api_version": "v1"
    }

@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    """Health check with configuration."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug
    }
```

**Configuration in Dependencies**:
```python
from sqlmodel import create_engine, Session

def get_engine(settings: Settings = Depends(get_settings)):
    """Create database engine from settings."""
    engine = create_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        echo=settings.database_echo
    )
    return engine

def get_db(engine = Depends(get_engine)) -> Generator[Session, None, None]:
    """Database session dependency."""
    with Session(engine) as session:
        yield session
```

### 4. Structured Logging

**Basic Logging Setup**:
```python
import logging
import sys
from typing import Any, Dict

def setup_logging(log_level: str = "INFO", log_format: str = "text") -> None:
    """
    Configure application logging.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Format type (text or json)
    """
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)

# Get logger for module
logger = logging.getLogger(__name__)

# Usage
logger.info("Application started")
logger.debug("Debug information", extra={"user_id": 123})
logger.error("Error occurred", exc_info=True)
```

**JSON Structured Logging**:
```python
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Outputs logs in JSON format for easy parsing by log aggregators.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        return json.dumps(log_data)


def setup_json_logging(log_level: str = "INFO") -> None:
    """
    Configure JSON structured logging for production.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.handlers = [handler]

    # Reduce noise from third-party libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Usage with extra fields
logger = logging.getLogger(__name__)
logger.info(
    "User logged in",
    extra={
        "request_id": "abc-123",
        "user_id": 456,
        "extra_data": {"ip": "192.168.1.1"}
    }
)
```

**Request ID Tracking Middleware**:
```python
import uuid
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from contextvars import ContextVar

# Context variable for request ID
request_id_var: ContextVar[str] = ContextVar("request_id", default="")

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add request ID to all requests.
    Enables request tracking across logs.
    """

    async def dispatch(self, request: Request, call_next):
        # Generate or extract request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store in context variable
        request_id_var.set(request_id)

        # Add to request state
        request.state.request_id = request_id

        # Process request
        response: Response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response


class RequestIDFilter(logging.Filter):
    """
    Logging filter to add request ID to log records.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get("")
        return True


# Setup with filter
def setup_logging_with_request_id(log_level: str = "INFO"):
    """Configure logging with request ID tracking."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    handler.addFilter(RequestIDFilter())

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.handlers = [handler]


# Add middleware to app
app.add_middleware(RequestIDMiddleware)
```

**Logging Utility Functions**:
```python
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

def log_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: Optional[int] = None
) -> None:
    """Log HTTP request with structured data."""
    logger.info(
        f"{method} {path} - {status_code}",
        extra={
            "extra_data": {
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "user_id": user_id
            }
        }
    )

def log_database_query(
    query_type: str,
    table: str,
    duration_ms: float,
    rows_affected: int = 0
) -> None:
    """Log database query with performance metrics."""
    logger.debug(
        f"DB {query_type} on {table}",
        extra={
            "extra_data": {
                "query_type": query_type,
                "table": table,
                "duration_ms": duration_ms,
                "rows_affected": rows_affected
            }
        }
    )

def log_external_api_call(
    service: str,
    endpoint: str,
    status_code: int,
    duration_ms: float,
    success: bool
) -> None:
    """Log external API call."""
    level = logging.INFO if success else logging.WARNING
    logger.log(
        level,
        f"External API: {service} {endpoint} - {status_code}",
        extra={
            "extra_data": {
                "service": service,
                "endpoint": endpoint,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "success": success
            }
        }
    )
```

### 5. Startup and Shutdown Logging

**Application Lifecycle Logging**:
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan with comprehensive logging.
    """
    # Startup
    logger.info("=" * 50)
    logger.info("Application starting up")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Log level: {settings.log_level}")
    logger.info("=" * 50)

    try:
        # Initialize database
        logger.info("Initializing database connection")
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database initialized successfully")

        # Initialize cache
        if settings.redis_url:
            logger.info("Connecting to Redis")
            await init_redis(settings.redis_url)
            logger.info("Redis connected successfully")

        # Log configuration (safe subset)
        logger.info("Configuration loaded", extra={
            "extra_data": {
                "app_name": settings.app_name,
                "environment": settings.environment,
                "api_prefix": settings.api_v1_prefix,
                "cors_origins": settings.cors_origins
            }
        })

        logger.info("Application startup complete")

    except Exception as e:
        logger.error(f"Startup failed: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("=" * 50)
    logger.info("Application shutting down")

    try:
        # Close database connections
        logger.info("Closing database connections")
        await engine.dispose()
        logger.info("Database connections closed")

        # Close Redis connections
        if settings.redis_url:
            logger.info("Closing Redis connections")
            await close_redis()
            logger.info("Redis connections closed")

        logger.info("Application shutdown complete")
        logger.info("=" * 50)

    except Exception as e:
        logger.error(f"Shutdown error: {e}", exc_info=True)


app = FastAPI(lifespan=lifespan)
```

**Startup Validation Logging**:
```python
def validate_configuration(settings: Settings) -> None:
    """
    Validate configuration at startup and log results.
    """
    logger.info("Validating configuration")

    errors = []
    warnings = []

    # Check required settings
    if settings.is_production:
        if settings.debug:
            warnings.append("Debug mode enabled in production")

        if "dev" in settings.secret_key.lower():
            errors.append("Development secret key used in production")

        if "*" in settings.cors_origins:
            warnings.append("CORS allows all origins in production")

    # Check database connection
    try:
        logger.info("Testing database connection")
        with Session(engine) as session:
            session.execute("SELECT 1")
        logger.info("Database connection successful")
    except Exception as e:
        errors.append(f"Database connection failed: {e}")

    # Log results
    if errors:
        for error in errors:
            logger.error(f"Configuration error: {error}")
        raise ValueError("Configuration validation failed")

    if warnings:
        for warning in warnings:
            logger.warning(f"Configuration warning: {warning}")

    logger.info("Configuration validation complete")


# Call during startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    validate_configuration(settings)
    yield
```

## Complete Integration Example

**main.py with Configuration and Logging**:
```python
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import time

from core.config import Settings, get_settings
from core.logging import (
    setup_json_logging,
    setup_logging_with_request_id,
    RequestIDMiddleware
)
from routers import users, auth

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with logging."""
    settings = get_settings()

    # Setup logging
    if settings.is_production:
        setup_json_logging(settings.log_level)
    else:
        setup_logging_with_request_id(settings.log_level)

    logger.info("Application starting", extra={
        "extra_data": {
            "environment": settings.environment,
            "debug": settings.debug
        }
    })

    yield

    logger.info("Application shutting down")


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Add middleware
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix=settings.api_v1_prefix)
    app.include_router(users.router, prefix=settings.api_v1_prefix)

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "environment": settings.environment
        }

    return app


app = create_app()
```

**core/config.py**:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    app_name: str = "FastAPI App"
    environment: str = "production"
    debug: bool = False
    log_level: str = "INFO"

    database_url: str = Field(...)
    secret_key: str = Field(..., min_length=32)

    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["*"]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

**core/logging.py**:
```python
import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


def setup_json_logging(log_level: str = "INFO"):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.handlers = [handler]
```

## Best Practices

### 1. Configuration Management
- Use `.env` files for local development
- Never commit `.env` to version control
- Commit `.env.example` with safe defaults
- Validate all configuration at startup
- Use Pydantic validators for type safety
- Cache settings with `@lru_cache()`
- Use different configs per environment

### 2. Secrets Management
- Never hardcode secrets in code
- Use environment variables for secrets
- Minimum 32 characters for secret keys
- Rotate secrets regularly
- Use secret management services in production (AWS Secrets Manager, HashiCorp Vault)
- Never log secrets or sensitive data

### 3. Logging Best Practices
- Use structured logging (JSON) in production
- Include request IDs for tracing
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Don't log sensitive data (passwords, tokens, PII)
- Log startup and shutdown events
- Log external API calls with timing
- Use correlation IDs for distributed tracing

### 4. Log Levels
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical messages for very serious errors

### 5. Production Considerations
- Use JSON logging for log aggregation
- Set appropriate log levels (INFO or WARNING in prod)
- Implement log rotation
- Send logs to centralized logging system
- Monitor log volume and costs
- Include performance metrics in logs

## Testing

### Configuration Testing
```python
import pytest
from core.config import Settings

def test_settings_validation():
    """Test settings validation."""
    # Valid settings
    settings = Settings(
        database_url="postgresql://localhost/test",
        secret_key="a" * 32,
        jwt_secret="b" * 32
    )
    assert settings.database_url.startswith("postgresql://")

    # Invalid database URL
    with pytest.raises(ValueError):
        Settings(
            database_url="invalid://url",
            secret_key="a" * 32,
            jwt_secret="b" * 32
        )

def test_environment_detection():
    """Test environment detection."""
    settings = Settings(
        environment="production",
        database_url="postgresql://localhost/test",
        secret_key="a" * 32,
        jwt_secret="b" * 32
    )
    assert settings.is_production is True
    assert settings.is_development is False
```

### Logging Testing
```python
import logging
from core.logging import JSONFormatter

def test_json_formatter():
    """Test JSON log formatting."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None
    )

    output = formatter.format(record)
    assert "timestamp" in output
    assert "Test message" in output
    assert "INFO" in output
```

## Summary

This skill provides comprehensive guidance for managing configuration and logging in FastAPI applications with:
- Environment-based configuration with Pydantic validation
- Type-safe settings with dependency injection
- Structured JSON logging for production
- Request ID tracking and correlation
- Startup/shutdown lifecycle logging
- Security best practices for secrets management
- Production-ready patterns for observability

Use this skill to ensure your FastAPI applications have robust configuration management and comprehensive logging for production environments.
