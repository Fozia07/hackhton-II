# Quickstart Guide: Database Integration with Neon PostgreSQL using SQLModel

## Overview
This guide provides instructions for setting up and using the database integration with Neon PostgreSQL in the backend application.

## Prerequisites
- Python 3.9+
- UV package manager
- Existing backend skeleton from feature 009-backend-skeleton
- Neon PostgreSQL database instance

## Setup Instructions

### 1. Configure Environment Variables
Update your `.env` file in `phaseII/backend/` with your Neon PostgreSQL connection details:
```
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 2. Install Dependencies
Make sure you have the backend virtual environment activated:
```bash
cd phaseII/backend
source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
```

The required dependencies should already be in your requirements.txt:
- sqlmodel
- psycopg2-binary
- python-dotenv

### 3. Verify Database Connection
Start the application to verify the database connection:
```bash
uv run uvicorn app.main:app --reload
```

## Usage

### Creating Database Models
New models should be created in the `phaseII/backend/app/models/` directory using SQLModel:
```python
from sqlmodel import SQLModel, Field

class NewModel(SQLModel, table=True):
    id: int = Field(primary_key=True)
    # Add other fields as needed
```

### Using Database Sessions
Database sessions are managed through FastAPI dependency injection in route handlers:
```python
from fastapi import Depends
from app.core.database import get_session

@app.get("/example")
def example_endpoint(session=Depends(get_session)):
    # Use the session for database operations
    pass
```

## Testing
To test the database integration:
1. Ensure your Neon PostgreSQL database is accessible
2. Start the application
3. Verify that the User table is created in your database
4. Check application logs for successful database connection messages

## Troubleshooting
- If the database connection fails, verify your DATABASE_URL is correct
- Ensure your Neon PostgreSQL instance allows connections from your environment
- Check that the required dependencies are installed in your virtual environment