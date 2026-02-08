"""
Custom exception classes for MCP tools in the Todo AI Chatbot.
Provides specific exception types for different error scenarios.
"""


class MCPToolError(Exception):
    """
    Base exception class for MCP tool errors.
    """
    def __init__(self, message: str, error_code: str = "MCP_TOOL_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert the exception to a dictionary for JSON serialization."""
        return {
            "error": self.message,
            "error_code": self.error_code
        }


class ValidationError(MCPToolError):
    """
    Raised when input validation fails.
    """
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR")


class DatabaseError(MCPToolError):
    """
    Raised when database operations fail.
    """
    def __init__(self, message: str):
        super().__init__(message, "DATABASE_ERROR")


class AuthorizationError(MCPToolError):
    """
    Raised when a user is not authorized to perform an operation.
    """
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, "AUTHORIZATION_ERROR")


class NotFoundError(MCPToolError):
    """
    Raised when a requested resource is not found.
    """
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND_ERROR")


class ConflictError(MCPToolError):
    """
    Raised when an operation conflicts with existing data.
    """
    def __init__(self, message: str = "Conflict with existing data"):
        super().__init__(message, "CONFLICT_ERROR")