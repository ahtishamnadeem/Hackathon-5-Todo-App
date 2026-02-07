"""JWT authentication middleware."""

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from app.services.auth import verify_token, extract_user_id
from app.utils.errors import UnauthorizedException

# HTTP Bearer token scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> int:
    """FastAPI dependency to extract and verify authenticated user from JWT token.

    This dependency should be added to all protected endpoints:
        @router.get("/protected")
        def protected_endpoint(user_id: int = Depends(get_current_user)):
            ...

    Args:
        credentials: HTTP Authorization header with Bearer token

    Returns:
        Authenticated user's ID

    Raises:
        UnauthorizedException: If token is missing, invalid, or expired

    Security (FR-007, FR-008, FR-009):
        - Validates JWT token signature
        - Checks token expiration
        - Extracts user_id from verified token
        - Rejects requests without valid tokens (401)
    """
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Missing authentication token")

    token = credentials.credentials

    try:
        # Verify token and extract user ID
        user_id = extract_user_id(token)
        return user_id
    except Exception as e:
        raise UnauthorizedException(f"Authentication failed: {str(e)}")


def get_optional_user(
    request: Request,
) -> Optional[int]:
    """Extract user ID from token if present, otherwise return None.

    Use this dependency for endpoints that work for both authenticated
    and unauthenticated users (e.g., public content with optional personalization).

    Args:
        request: FastAPI request object

    Returns:
        User ID if authenticated, None otherwise
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")

    try:
        user_id = extract_user_id(token)
        return user_id
    except:
        return None
