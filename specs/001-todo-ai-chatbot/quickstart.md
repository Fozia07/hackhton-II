# Todo AI Chatbot - Quickstart Guide

## Phase III Backend Setup

### Prerequisites
- Python 3.9+
- Poetry or pip for dependency management
- Access to Neon PostgreSQL database
- Phase II backend running (for reference and authentication)

### 1. Initialize the Project Structure
```bash
# Create the Phase III backend directory
mkdir -p phaseIII/backend
cd phaseIII/backend

# Initialize a new Python project
poetry init
poetry add fastapi sqlmodel alembic psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart uvicorn
poetry add -D pytest pytest-asyncio httpx black flake8 mypy
```

### 2. Set Up Database Models
Create the database models based on the data-model.md specification:

```bash
# Create directory structure
mkdir -p app/models app/database app/schemas app/api app/core
```

### 3. Configure Database Connection
Create `app/database/session.py`:
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os

DATABASE_URL = os.getenv("NEON_DATABASE_URL", "")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session
```

### 4. Set Up Alembic for Migrations
```bash
alembic init -t async alembic
```

Configure `alembic.ini` to use async operations and update `alembic/env.py` to work with SQLModel.

### 5. Create the Data Models
Based on the data-model.md specification, implement the SQLModel models in `app/models/`.

### 6. Implement MCP Tools API
Create the 5 required MCP tools as specified in the contracts:
- POST `/mcp/add_task`
- POST `/mcp/list_tasks`
- POST `/mcp/complete_task`
- POST `/mcp/delete_task`
- POST `/mcp/update_task`

### 7. Run Migrations
```bash
alembic revision --autogenerate -m "Initial Phase III tables"
alembic upgrade head
```

### 8. Start the Development Server
```bash
uvicorn app.main:app --reload --port 8001
```

## Environment Variables
Create a `.env` file in the Phase III backend directory:
```env
NEON_DATABASE_URL=your_neon_db_url_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Testing
Run the test suite to ensure all components work correctly:
```bash
poetry run pytest
```

## Security Considerations
- All MCP tools must verify user authentication via JWT
- All database queries must include user_id scoping
- Input validation must be performed on all endpoints
- Rate limiting should be implemented for MCP tool endpoints