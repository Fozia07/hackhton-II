from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Phase 2 Backend"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: Optional[str] = None
    allowed_origins: str = "https://hackhton-ii.vercel.app,http://localhost:3000,http://localhost:3001,http://localhost:3002"  # Comma-separated list of origins

    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()