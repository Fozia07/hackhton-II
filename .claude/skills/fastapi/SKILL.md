---
name: fastapi
description: |
  Builds Python APIs with FastAPI from hello world to professional production systems.
  This skill should be used when users want to create REST APIs, build web services with Python,
  implement async endpoints, add authentication and authorization, integrate databases with SQLAlchemy,
  create WebSocket connections, handle file uploads, or deploy production-ready FastAPI applications.
  Handles path operations, dependency injection, Pydantic models, testing, and deployment patterns.
---

# FastAPI

Build modern, fast Python APIs from hello world to production systems.

## What This Skill Does

- Creates FastAPI applications with path operations (GET, POST, PUT, DELETE)
- Implements request/response models with Pydantic validation
- Sets up dependency injection for reusable components
- Integrates databases with SQLAlchemy (sync and async)
- Implements authentication (OAuth2, JWT, API keys)
- Handles file uploads, WebSockets, background tasks
- Provides testing patterns with TestClient
- Offers production deployment strategies

## What This Skill Does NOT Do

- Build frontend applications (FastAPI is backend-only)
- Handle non-Python backends
- Manage infrastructure provisioning
- Deploy to specific cloud providers (provides patterns only)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI apps, database models, project structure |
| **Conversation** | User's requirements: API type, features, database, authentication |
| **Skill References** | FastAPI patterns from `references/` (basics, database, auth, deployment) |
| **User Guidelines** | Team conventions, security requirements, tech stack |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Core Architecture

### How FastAPI Works

```
HTTP Request
    ↓
FastAPI Router
    ↓
Path Operation Function
    ↓
Dependencies (if any)
    ↓
Request Validation (Pydantic)
    ↓
Business Logic
    ↓
Response Model (Pydantic)
    ↓
HTTP Response (JSON)
```

### Key Components

| Component | Purpose | Technology |
|-----------|---------|------------|
| **Path Operations** | HTTP endpoints (GET, POST, etc.) | Decorators (@app.get, @app.post) |
| **Pydantic Models** | Request/response validation | Pydantic BaseModel |
| **Dependencies** | Reusable logic (auth, DB) | Depends() |
| **Middleware** | Request/response processing | ASGI middleware |
| **Background Tasks** | Async operations | BackgroundTasks |
| **Database** | Data persistence | SQLAlchemy (sync/async) |

---

## Implementation Levels

Progressive complexity for different use cases:

| Level | Capability | When to Use |
|-------|-----------|-------------|
| **Hello World** | Simple GET endpoint | Learning, prototyping |
| **CRUD API** | Create, Read, Update, Delete | Basic data APIs |
| **With Database** | SQLAlchemy integration | Persistent data |
| **With Auth** | OAuth2/JWT authentication | Secure APIs |
| **Production** | Testing, deployment, monitoring | Real applications |

---

## Core Workflow

### 1. Clarify Requirements

Ask user about THEIR specific needs:

| Question | Purpose |
|----------|---------|
| **API type** | REST API, WebSocket, or both? |
| **Data operations** | CRUD, read-only, or complex operations? |
| **Database** | PostgreSQL, MySQL, SQLite, or none? |
| **Authentication** | Public, API keys, OAuth2, or JWT? |
| **File handling** | File uploads/downloads needed? |
| **Async** | Async operations (database, external APIs)? |

### 2. Choose Architecture Pattern

Based on requirements, select from `references/basics.md`:

- **Simple API**: Path operations with in-memory data
- **CRUD API**: Full Create, Read, Update, Delete operations
- **Database API**: SQLAlchemy integration
- **Authenticated API**: OAuth2/JWT security
- **Production API**: Full error handling, testing, deployment

### 3. Set Up FastAPI Application

Create basic FastAPI app:

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="API description",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 4. Define Pydantic Models

Create request/response models:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(..., gt=0)
    tax: float | None = None
```

### 5. Implement Path Operations

Create endpoints:

```python
@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    # Business logic
    return item

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    # Fetch from database
    return item
```

### 6. Add Dependencies

Implement reusable logic:

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

### 7. Add Authentication (Optional)

Implement security:

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Verify token
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

### 8. Test and Deploy

- Write tests with TestClient
- Add error handling and logging
- Configure CORS if needed
- Deploy with Uvicorn/Gunicorn

---

## Quick Start Examples

### Hello World

Simplest FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Run with:
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

### CRUD API

Basic Create, Read, Update, Delete:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items = {}

@app.post("/items/", status_code=201)
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, **item.dict()}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = item
    return item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
```

See `references/basics.md` for complete examples.

---

## Key Concepts

### Path Operations

HTTP methods mapped to functions:

```python
@app.get("/items/")      # Read list
@app.post("/items/")     # Create
@app.get("/items/{id}")  # Read one
@app.put("/items/{id}")  # Update
@app.delete("/items/{id}") # Delete
```

### Path Parameters

Variables in URL path:

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Query Parameters

Optional parameters after `?`:

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]
```

### Request Body

Data sent in POST/PUT requests:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Response Models

Define response structure:

```python
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    return get_item_from_db(item_id)
```

### Dependencies

Reusable components:

```python
from fastapi import Depends

def common_parameters(q: str | None = None, skip: int = 0):
    return {"q": q, "skip": skip}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### Validation

Automatic with Pydantic:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    tags: list[str] = []
```

---

## Common Patterns

### Pattern: Pagination

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return items[skip : skip + limit]
```

### Pattern: Error Handling

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    item = get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return item
```

### Pattern: File Upload

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "size": len(contents)
    }
```

### Pattern: Background Tasks

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification sent to {email}")
    return {"message": "Notification sent"}
```

### Pattern: CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

See `references/basics.md` for complete patterns.

---

## Dependencies

### Required

```bash
pip install fastapi uvicorn[standard]
```

### Optional

```bash
# Database
pip install sqlalchemy psycopg2-binary  # PostgreSQL
pip install sqlalchemy pymysql          # MySQL

# Authentication
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# Testing
pip install pytest httpx

# Production
pip install gunicorn
```

---

## Production Checklist

Before deploying to production:

- [ ] Add comprehensive error handling
- [ ] Implement request validation with Pydantic
- [ ] Add authentication and authorization
- [ ] Configure CORS properly
- [ ] Set up database connection pooling
- [ ] Add logging and monitoring
- [ ] Write tests (unit and integration)
- [ ] Configure environment variables
- [ ] Set up rate limiting
- [ ] Add API documentation
- [ ] Configure HTTPS
- [ ] Set up CI/CD pipeline

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **422 Validation Error** | Check request body matches Pydantic model |
| **404 Not Found** | Verify path and path parameters |
| **500 Internal Server Error** | Check logs, add error handling |
| **CORS errors** | Configure CORSMiddleware |
| **Import errors** | Install all required packages |
| **Database connection errors** | Check connection string and credentials |

### Debug Mode

Enable detailed error messages:

```python
from fastapi import FastAPI

app = FastAPI(debug=True)
```

View logs:
```bash
uvicorn main:app --reload --log-level debug
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/basics.md` | Path operations, parameters, models, validation |
| `references/database.md` | SQLAlchemy integration, async database operations |
| `references/auth-security.md` | OAuth2, JWT, dependencies, security patterns |
| `references/testing-deployment.md` | Testing, deployment, production patterns |

---

## Example: Complete CRUD API

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Items API", version="1.0.0")

# Models
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(..., gt=0)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True

# In-memory database
items_db = {}
next_id = 1

# CRUD Operations
@app.post("/items/", response_model=Item, status_code=201, tags=["items"])
async def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    item_dict = item.dict()
    item_dict["id"] = next_id
    items_db[next_id] = item_dict
    next_id += 1
    return item_dict

@app.get("/items/", response_model=List[Item], tags=["items"])
async def read_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination"""
    items = list(items_db.values())
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item, tags=["items"])
async def read_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item, tags=["items"])
async def update_item(item_id: int, item: ItemCreate):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_dict = item.dict()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict
    return item_dict

@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]

# Health check
@app.get("/health", tags=["system"])
async def health_check():
    """Check API health"""
    return {"status": "healthy"}
```

Run with:
```bash
uvicorn main:app --reload
```

Visit:
- API docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

---

## Next Steps

After implementing basic API:

1. **Add Database**: Integrate SQLAlchemy for persistence
2. **Add Authentication**: Implement OAuth2/JWT
3. **Add Tests**: Write unit and integration tests
4. **Add Middleware**: Logging, rate limiting, compression
5. **Add WebSockets**: Real-time communication
6. **Deploy**: Follow production deployment patterns
7. **Monitor**: Add logging and metrics
8. **Iterate**: Improve based on usage

See reference files for detailed guidance on each step.
