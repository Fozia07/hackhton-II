# Database Integration

Comprehensive guide to integrating databases with FastAPI using SQLAlchemy (sync and async).

---

## SQLAlchemy Setup (Sync)

### Installation

```bash
pip install sqlalchemy psycopg2-binary  # PostgreSQL
# or
pip install sqlalchemy pymysql          # MySQL
```

### Database Configuration

**database.py**:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# For SQLite: "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # For SQLite only:
    # connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

### Database Models

**models.py**:
```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
```

### Pydantic Schemas

**schemas.py**:
```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True
```

### Database Dependency

**main.py**:
```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## CRUD Operations

### Create

```python
from sqlalchemy.orm import Session
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
```

### Read

```python
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
```

### Update

```python
def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item
```

### Delete

```python
def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
```

---

## FastAPI Endpoints with Database

```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
```

---

## Async SQLAlchemy

### Installation

```bash
pip install sqlalchemy[asyncio] asyncpg  # PostgreSQL
# or
pip install sqlalchemy[asyncio] aiomysql  # MySQL
```

### Async Database Configuration

**database.py**:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()
```

### Async Models

Same as sync models (models.py remains the same).

### Async CRUD Operations

**crud.py**:
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User).filter(models.User.id == user_id)
    )
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserCreate):
    result = await db.execute(
        select(models.User).filter(models.User.id == user_id)
    )
    db_user = result.scalars().first()
    if db_user:
        db_user.email = user.email
        db_user.hashed_password = user.password + "notreallyhashed"
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User).filter(models.User.id == user_id)
    )
    db_user = result.scalars().first()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
```

### Async FastAPI Endpoints

**main.py**:
```python
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud, models, schemas
from database import AsyncSessionLocal, engine

app = FastAPI()

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    db_user = await crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
```

---

## Advanced Queries

### Filtering

```python
from sqlalchemy import and_, or_

async def get_items_by_filters(
    db: AsyncSession,
    min_price: float | None = None,
    max_price: float | None = None,
    owner_id: int | None = None
):
    query = select(models.Item)

    filters = []
    if min_price is not None:
        filters.append(models.Item.price >= min_price)
    if max_price is not None:
        filters.append(models.Item.price <= max_price)
    if owner_id is not None:
        filters.append(models.Item.owner_id == owner_id)

    if filters:
        query = query.filter(and_(*filters))

    result = await db.execute(query)
    return result.scalars().all()
```

### Sorting

```python
from sqlalchemy import desc

async def get_items_sorted(
    db: AsyncSession,
    sort_by: str = "title",
    order: str = "asc"
):
    query = select(models.Item)

    if order == "desc":
        query = query.order_by(desc(getattr(models.Item, sort_by)))
    else:
        query = query.order_by(getattr(models.Item, sort_by))

    result = await db.execute(query)
    return result.scalars().all()
```

### Joins

```python
from sqlalchemy.orm import selectinload

async def get_users_with_items(db: AsyncSession):
    result = await db.execute(
        select(models.User).options(selectinload(models.User.items))
    )
    return result.scalars().all()
```

### Aggregations

```python
from sqlalchemy import func

async def get_item_count_by_user(db: AsyncSession):
    result = await db.execute(
        select(
            models.User.email,
            func.count(models.Item.id).label("item_count")
        )
        .join(models.Item)
        .group_by(models.User.email)
    )
    return result.all()
```

---

## Transactions

### Manual Transaction Control

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def transfer_item(
    db: AsyncSession,
    item_id: int,
    from_user_id: int,
    to_user_id: int
):
    async with db.begin():
        # Get item
        result = await db.execute(
            select(models.Item).filter(models.Item.id == item_id)
        )
        item = result.scalars().first()

        if not item or item.owner_id != from_user_id:
            raise ValueError("Item not found or not owned by user")

        # Transfer ownership
        item.owner_id = to_user_id
        await db.commit()

    return item
```

### Rollback on Error

```python
async def create_user_with_items(
    db: AsyncSession,
    user: schemas.UserCreate,
    items: list[schemas.ItemCreate]
):
    try:
        async with db.begin():
            # Create user
            db_user = models.User(
                email=user.email,
                hashed_password=user.password + "notreallyhashed"
            )
            db.add(db_user)
            await db.flush()  # Get user.id without committing

            # Create items
            for item in items:
                db_item = models.Item(**item.dict(), owner_id=db_user.id)
                db.add(db_item)

            await db.commit()
            await db.refresh(db_user)
            return db_user
    except Exception as e:
        await db.rollback()
        raise e
```

---

## Connection Pooling

### Configuration

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,           # Number of connections to maintain
    max_overflow=10,        # Additional connections under load
    pool_timeout=30,        # Wait time for connection
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Verify connections before use
)
```

---

## Migrations with Alembic

### Installation

```bash
pip install alembic
```

### Initialize Alembic

```bash
alembic init alembic
```

### Configure Alembic

**alembic.ini**:
```ini
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

**alembic/env.py**:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import models  # Import your models

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
fileConfig(config.config_file_name)

# Set target metadata
target_metadata = models.Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Create Migration

```bash
alembic revision --autogenerate -m "Create users and items tables"
```

### Apply Migration

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

---

## Database Best Practices

### 1. Use Connection Pooling

```python
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True
)
```

### 2. Use Indexes

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # Index for lookups
    created_at = Column(DateTime, index=True)        # Index for sorting
```

### 3. Use Lazy Loading Wisely

```python
# Eager loading (better for known relationships)
result = await db.execute(
    select(models.User).options(selectinload(models.User.items))
)

# Lazy loading (default, loads on access)
user = await get_user(db, user_id)
items = user.items  # Triggers additional query
```

### 4. Use Pagination

```python
@app.get("/items/")
async def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(models.Item).offset(skip).limit(limit)
    )
    return result.scalars().all()
```

### 5. Handle Exceptions

```python
from sqlalchemy.exc import IntegrityError

@app.post("/users/")
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
```

---

## Complete Example with Database

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    items = relationship("Item", back_populates="owner")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")


# schemas.py
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: list[Item] = []
    class Config:
        from_attributes = True


# crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password + "notreallyhashed"
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()


# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import crud, models, schemas
from database import AsyncSessionLocal, engine

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await crud.get_users(db, skip=skip, limit=limit)
```

Run with:
```bash
uvicorn main:app --reload
```
