# FastAPI Basics

Comprehensive guide to FastAPI fundamentals: path operations, parameters, models, and validation.

---

## Path Operations

### Basic Path Operations

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(name: str, price: float):
    return {"name": name, "price": price}

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str):
    return {"item_id": item_id, "name": name}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"deleted": item_id}
```

---

### Path Operation Configuration

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create an item",
    description="Create a new item with all the information",
    response_description="The created item",
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    """
    return item
```

---

### Multiple Path Operations

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

**Order matters**: More specific paths must come before generic ones.

---

## Path Parameters

### Basic Path Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

### Path Parameters with Validation

```python
from fastapi import Path

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000)
):
    return {"item_id": item_id}
```

### Enum Path Parameters

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
```

### File Path Parameters

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
```

---

## Query Parameters

### Basic Query Parameters

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

### Optional Query Parameters

```python
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Query Parameters with Validation

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    q: str | None = Query(
        None,
        min_length=3,
        max_length=50,
        pattern="^fixedquery$",
        title="Query string",
        description="Query string for the items to search"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

### Required Query Parameters

```python
@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    results.update({"q": q})
    return results
```

### Multiple Query Parameters

```python
@app.get("/items/")
async def read_items(
    q: str | None = None,
    skip: int = 0,
    limit: int = 10,
    sort: str = "asc"
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort": sort
    }
```

### List Query Parameters

```python
@app.get("/items/")
async def read_items(q: list[str] | None = Query(None)):
    query_items = {"q": q}
    return query_items
```

URL: `/items/?q=foo&q=bar`

---

## Request Body

### Pydantic Models

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Request Body + Path Parameters

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}
```

### Request Body + Path + Query Parameters

```python
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    q: str | None = None
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
```

### Multiple Body Parameters

```python
class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    full_name: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}
```

### Singular Values in Body

```python
from fastapi import Body

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(...)
):
    return {"item_id": item_id, "item": item, "user": user, "importance": importance}
```

---

## Pydantic Models

### Basic Model

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
```

### Model with Validation

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    tax: float | None = Field(None, ge=0, le=100)
    tags: list[str] = []
```

### Nested Models

```python
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None

@app.post("/items/")
async def create_item(item: Item):
    return item
```

### Model Configuration

```python
class Item(BaseModel):
    name: str
    price: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4
            }
        }
```

### Model Inheritance

```python
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
```

---

## Response Models

### Basic Response Model

```python
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
```

### Response Model with Filtering

```python
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: str
    full_name: str | None = None

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user  # Password is automatically filtered out
```

### List Response Model

```python
@app.get("/items/", response_model=list[Item])
async def read_items():
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
```

### Response Model with Status Code

```python
from fastapi import status

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

### Multiple Response Models

```python
from fastapi.responses import JSONResponse

class Message(BaseModel):
    message: str

@app.get(
    "/items/{item_id}",
    response_model=Item,
    responses={
        404: {"model": Message, "description": "Item not found"},
        200: {"description": "Item found"}
    }
)
async def read_item(item_id: int):
    if item_id not in items:
        return JSONResponse(
            status_code=404,
            content={"message": "Item not found"}
        )
    return items[item_id]
```

---

## Error Handling

### HTTPException

```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]
```

### Custom Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong"}
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

### Override Default Exception Handlers

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)
```

---

## File Uploads

### Single File Upload

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }
```

### Multiple File Uploads

```python
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {
        "filenames": [file.filename for file in files]
    }
```

### File Upload with Additional Data

```python
@app.post("/files/")
async def create_file(
    file: UploadFile,
    token: str = Form(...),
    description: str = Form(None)
):
    return {
        "filename": file.filename,
        "token": token,
        "description": description
    }
```

### Save Uploaded File

```python
import shutil
from pathlib import Path

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "location": str(file_path)}
```

---

## Background Tasks

### Basic Background Task

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
    return {"message": "Notification sent in the background"}
```

### Multiple Background Tasks

```python
def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

def send_email(email: str, message: str):
    # Send email logic
    pass

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_log, f"Notification to {email}")
    background_tasks.add_task(send_email, email, "Your notification")
    return {"message": "Notification sent"}
```

### Background Task with Dependencies

```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_analytics(item_id: int, db):
    # Update analytics in database
    pass

@app.post("/items/{item_id}/view")
async def view_item(
    item_id: int,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    background_tasks.add_task(update_analytics, item_id, db)
    return {"message": "View recorded"}
```

---

## CORS

### Basic CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Specific Origins

```python
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Specific Methods and Headers

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

---

## WebSockets

### Basic WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
```

### WebSocket with Connection Manager

```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
```

---

## Middleware

### Custom Middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### Logging Middleware

```python
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
```

### Authentication Middleware

```python
@app.middleware("http")
async def authenticate(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        token = request.headers.get("Authorization")
        if not token or not verify_token(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Unauthorized"}
            )
    response = await call_next(request)
    return response
```

---

## Dependencies

### Basic Dependency

```python
from fastapi import Depends

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-Based Dependency

```python
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 10):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    return commons
```

### Sub-Dependencies

```python
def query_extractor(q: str | None = None):
    return q

def query_or_default(query: str = Depends(query_extractor)):
    if not query:
        return "default"
    return query

@app.get("/items/")
async def read_items(query: str = Depends(query_or_default)):
    return {"query": query}
```

### Dependencies with yield

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

### Global Dependencies

```python
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

app = FastAPI(dependencies=[Depends(verify_token)])
```

---

## Complete CRUD Example

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="Complete CRUD API")

# Models
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    tax: float | None = Field(None, ge=0, le=100)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0)
    tax: float | None = Field(None, ge=0, le=100)

class Item(ItemBase):
    id: int

# Database (in-memory)
items_db = {}
next_id = 1

# CRUD Operations
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    """Create a new item"""
    global next_id
    item_dict = item.dict()
    item_dict["id"] = next_id
    items_db[next_id] = item_dict
    next_id += 1
    return item_dict

@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    """Get all items with pagination"""
    items = list(items_db.values())
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    """Get a specific item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    stored_item = items_db[item_id]
    update_data = item.dict(exclude_unset=True)
    updated_item = {**stored_item, **update_data}
    items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    del items_db[item_id]
```

---

## Best Practices

### 1. Use Type Hints

```python
# Good
@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict:
    return {"item_id": item_id}

# Better
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int) -> Item:
    return get_item(item_id)
```

### 2. Use Pydantic for Validation

```python
# Good
class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
```

### 3. Use Dependencies

```python
# Reusable logic
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db = Depends(get_db)):
    return db.query(Item).all()
```

### 4. Use Status Codes

```python
from fastapi import status

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item
```

### 5. Document Your API

```python
@app.post(
    "/items/",
    summary="Create an item",
    description="Create a new item with all the information",
    response_description="The created item"
)
async def create_item(item: Item):
    """
    Create an item with:
    - **name**: required
    - **price**: required, must be positive
    """
    return item
```

---

## Common Patterns

### Pagination

```python
from fastapi import Query

@app.get("/items/")
async def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return items[skip : skip + limit]
```

### Filtering

```python
@app.get("/items/")
async def read_items(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None
):
    filtered_items = items
    if category:
        filtered_items = [i for i in filtered_items if i.category == category]
    if min_price:
        filtered_items = [i for i in filtered_items if i.price >= min_price]
    if max_price:
        filtered_items = [i for i in filtered_items if i.price <= max_price]
    return filtered_items
```

### Sorting

```python
@app.get("/items/")
async def read_items(
    sort_by: str = "name",
    order: str = "asc"
):
    sorted_items = sorted(
        items,
        key=lambda x: getattr(x, sort_by),
        reverse=(order == "desc")
    )
    return sorted_items
```
