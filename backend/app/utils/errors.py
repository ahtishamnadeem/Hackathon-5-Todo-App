"""Custom exception classes and error handlers."""

from typing import Optional, Dict, Any


class TodoAppException(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class UnauthorizedException(TodoAppException):
    """Raised when authentication fails or token is invalid."""

    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, error_code="UNAUTHORIZED", status_code=401, details=details
        )


class ValidationException(TodoAppException):
    """Raised when input validation fails."""

    def __init__(
        self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message, error_code="VALIDATION_ERROR", status_code=400, details=details
        )


class NotFoundException(TodoAppException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message, error_code="NOT_FOUND", status_code=404, details=details
        )


class DatabaseException(TodoAppException):
    """Raised when a database operation fails."""

    def __init__(
        self, message: str = "Database error", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message, error_code="DATABASE_ERROR", status_code=500, details=details
        )


class DuplicateEmailException(TodoAppException):
    """Raised when attempting to register with an existing email."""

    def __init__(
        self, message: str = "Email already registered", details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message, error_code="DUPLICATE_EMAIL", status_code=400, details=details
        )


class InvalidCredentialsException(TodoAppException):
    """Raised when login credentials are incorrect."""

    def __init__(
        self,
        message: str = "Invalid email or password",
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message, error_code="INVALID_CREDENTIALS", status_code=400, details=details
        )


def format_error_response(
    error_code: str, message: str, details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Format error response according to contracts/errors.md specification.

    Returns standardized error response:
    {
        "success": false,
        "data": null,
        "error": {
            "code": "ERROR_CODE",
            "message": "Human-readable error message",
            "details": {}
        }
    }
    """
    return {
        "success": False,
        "data": None,
        "error": {"code": error_code, "message": message, "details": details or {}},
    }
