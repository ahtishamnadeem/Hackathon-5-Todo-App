"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session

from app.database import get_session
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.services.auth import register_user, login_user
from app.utils.errors import format_error_response
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user account",
    description="Create a new user account with email and password. Returns JWT token on success.",
)
def register(
    request: RegisterRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    """Register a new user account.

    Request Body:
        - email: Valid email address (must be unique)
        - password: Minimum 8 characters, at least one letter and one number

    Response:
        - 201 Created: Account created, JWT token issued
        - 400 Bad Request: Validation error or duplicate email

    Security (FR-001, FR-002, FR-003, FR-004, FR-006, FR-010):
        - Validates email format (Pydantic)
        - Enforces password requirements (Pydantic validator)
        - Checks for duplicate email
        - Hashes password with bcrypt before storage
        - Issues JWT token immediately
        - Stores token in httpOnly cookie
    """
    try:
        # Register user
        user = register_user(request.email, request.password, session)

        # Generate token
        from app.services.auth import create_access_token
        token = create_access_token(user.id, user.email)

        # Set httpOnly cookie (FR-010)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  # Prevents JavaScript access (XSS protection)
            secure=False,  # Set to True in production (HTTPS only)
            samesite="lax",  # CSRF protection
            max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        )

        return TokenResponse(
            success=True,
            data={
                "message": "Registration successful",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
        )

    except Exception as e:
        # Error handling will be done by global exception handler
        raise


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
    description="Login with email and password. Returns JWT token on success.",
)
def login(
    request: LoginRequest,
    response: Response,
    session: Session = Depends(get_session),
):
    """Authenticate user and issue JWT token.

    Request Body:
        - email: User's email address
        - password: User's password

    Response:
        - 200 OK: Authentication successful, JWT token issued
        - 400 Bad Request: Invalid credentials

    Security (FR-005, FR-006, FR-010):
        - Validates credentials
        - Generates JWT token with expiration
        - Stores token in httpOnly cookie
        - Returns same error for invalid email or password (prevents enumeration)
    """
    try:
        # Authenticate user
        user, token = login_user(request.email, request.password, session)

        # Set httpOnly cookie (FR-010)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,  # Prevents JavaScript access (XSS protection)
            secure=False,  # Set to True in production (HTTPS only)
            samesite="lax",  # CSRF protection
            max_age=7 * 24 * 60 * 60,  # 7 days in seconds
        )

        return TokenResponse(
            success=True,
            data={
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                },
            },
        )

    except Exception as e:
        # Error handling will be done by global exception handler
        raise


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="Terminate user session",
    description="Logout user by clearing JWT token cookie.",
)
def logout(response: Response):
    """Terminate user session and clear JWT token.

    Response:
        - 200 OK: Session terminated successfully

    Security (FR-011):
        - Clears httpOnly cookie
        - Immediately invalidates client-side token
    """
    # Clear the httpOnly cookie
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=False,  # Set to True in production
        samesite="lax",
    )

    return {
        "success": True,
        "data": {"message": "Logout successful"},
        "error": None,
    }


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user information",
    description="Retrieve authenticated user's profile information.",
)
def get_me(
    user_id: int = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get current authenticated user's information.

    Response:
        - 200 OK: User information retrieved successfully
        - 401 Unauthorized: Invalid or missing token

    Security:
        - Requires valid JWT token
        - Returns only authenticated user's own data
    """
    user = session.get(User, user_id)

    if not user:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "USER_NOT_FOUND",
                "message": "User not found",
                "details": {}
            }
        }

    return {
        "success": True,
        "data": {
            "user": {
                "id": user.id,
                "email": user.email,
            }
        },
        "error": None,
    }
