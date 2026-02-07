"""
Configuration settings for the Todo AI Chatbot.
Contains settings for OpenAI API, MCP client, and JWT authentication.
"""
import os
from typing import Optional
from pydantic import BaseModel


class AIConfig(BaseModel):
    """
    Configuration for AI API settings (OpenAI and Gemini).
    """
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    gemini_base_url: str = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    openai_model: str = os.getenv("OPENAI_MODEL", "gemini-1.5-flash")
    temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
    timeout: int = int(os.getenv("OPENAI_TIMEOUT", "30"))


class JWTConfig(BaseModel):
    """
    Configuration for JWT authentication settings.
    """
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "47fa85fedc6d1dd46053ff3f5618f191"))
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


class MCPConfig(BaseModel):
    """
    Configuration for MCP server settings.
    """
    mcp_server_url: str = os.getenv("MCP_SERVER_URL", "http://localhost:8002")
    mcp_timeout: int = int(os.getenv("MCP_TIMEOUT", "30"))
    mcp_retry_attempts: int = int(os.getenv("MCP_RETRY_ATTEMPTS", "3"))
    mcp_transport: str = os.getenv("MCP_TRANSPORT", "http")


class AppConfig:
    """
    Main application configuration combining all settings.
    """
    def __init__(self):
        self.ai_config = AIConfig()
        self.mcp_config = MCPConfig()
        self.jwt_config = JWTConfig()

        # Validate required settings
        if not self.ai_config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        if not self.mcp_config.mcp_server_url:
            raise ValueError("MCP_SERVER_URL environment variable is required")

    @property
    def openai_api_key(self) -> str:
        return self.ai_config.openai_api_key

    @property
    def gemini_api_key(self) -> str:
        return self.ai_config.gemini_api_key

    @property
    def openai_base_url(self) -> str:
        return self.ai_config.openai_base_url

    @property
    def gemini_base_url(self) -> str:
        return self.ai_config.gemini_base_url

    @property
    def openai_model(self) -> str:
        return self.ai_config.openai_model

    @property
    def ai_temperature(self) -> float:
        return self.ai_config.temperature

    @property
    def ai_max_tokens(self) -> int:
        return self.ai_config.max_tokens

    @property
    def mcp_server_url(self) -> str:
        return self.mcp_config.mcp_server_url

    @property
    def mcp_timeout(self) -> int:
        return self.mcp_config.mcp_timeout

    @property
    def mcp_retry_attempts(self) -> int:
        return self.mcp_config.mcp_retry_attempts

    @property
    def jwt_secret_key(self) -> str:
        return self.jwt_config.jwt_secret_key

    @property
    def jwt_algorithm(self) -> str:
        return self.jwt_config.jwt_algorithm

    @property
    def access_token_expire_minutes(self) -> int:
        return self.jwt_config.access_token_expire_minutes


# Global configuration instance
config = AppConfig()