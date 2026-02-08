from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import AsyncAdaptedQueuePool  # ← Add this import
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")

import urllib.parse

# Parse the database URL to determine the type
parsed_url = urllib.parse.urlparse(DATABASE_URL)

# Configure connect_args based on database type
if parsed_url.scheme.startswith('postgresql'):
    connect_kwargs = {
        "server_settings": {
            "application_name": "phaseIII-backend",
        }
    }
else:
    # SQLite and other databases don't support server_settings
    connect_kwargs = {}

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    poolclass=AsyncAdaptedQueuePool,  # ← Async-safe pool
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=300,
    connect_args=connect_kwargs
)