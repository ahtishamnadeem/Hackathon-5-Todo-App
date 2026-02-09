"""FastAPI application entry point."""

from fastapi import FastAPI, Request, status, Depends
from app.middleware.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import FRONTEND_URL
from app.routers import auth_router, todos_router, chat_router
from app.utils.errors import (
    TodoAppException,
    UnauthorizedException,
    ValidationException,
    NotFoundException,
    DatabaseException,
    format_error_response,
)

# Create FastAPI application
app = FastAPI(
    title="Todo Full-Stack Web Application API",
    description="Secure, multi-user todo management API with JWT authentication",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware (FR-027)
# Allow all localhost and 127.0.0.1 origins for local development
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:30000",
    "http://127.0.0.1:50129",
    "http://127.0.0.1:64865",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow specific local origins
    allow_credentials=True,  # Allow cookies (for httpOnly JWT tokens)
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


# Register routers (T053)
app.include_router(auth_router, prefix="/api")
app.include_router(todos_router, prefix="/api", dependencies=[Depends(get_current_user)])
app.include_router(chat_router, prefix="/api", dependencies=[Depends(get_current_user)])


# Global exception handlers (T054)
@app.exception_handler(TodoAppException)
async def todo_app_exception_handler(request: Request, exc: TodoAppException):
    """Handle custom application exceptions.

    Returns standardized error response per contracts/errors.md (FR-029)
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
        ),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions.

    Returns generic 500 error without exposing internal details (FR-028)
    """
    # Log the actual error (in production, use proper logging)
    print(f"Unexpected error: {type(exc).__name__}: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_error_response(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            details={},
        ),
    )


# Root endpoint
@app.get("/", tags=["Health"])
def root():
    """API health check endpoint."""
    return {
        "success": True,
        "data": {
            "message": "Todo API v2.0.0",
            "status": "operational",
            "docs": "/docs",
        },
        "error": None,
    }


# Startup event
@app.on_event("startup")
def on_startup():
    """Application startup event handler."""
    from app.config import settings
    from app.database import create_db_and_tables

    # Validate configuration
    try:
        settings.validate()
        print("[OK] Configuration validated successfully")
    except ValueError as e:
        print(f"[ERROR] Configuration error: {str(e)}")
        raise

    # Create database tables
    try:
        create_db_and_tables()
        print("[OK] Database tables created successfully")
    except Exception as e:
        print(f"[ERROR] Database initialization error: {str(e)}")
        raise

    print(f"[START] Todo API starting on {settings.HOST}:{settings.PORT}")
    print(f"[DOCS] API docs available at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"[CORS] CORS enabled for: {', '.join(allowed_origins)}")
