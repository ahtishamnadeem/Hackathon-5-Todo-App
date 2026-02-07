"""Authentication service layer."""

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select

from app.config import BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, BCRYPT_WORK_FACTOR
from app.models.user import User
from app.utils.errors import (
    DuplicateEmailException,
    InvalidCredentialsException,
    UnauthorizedException,
)


def hash_password(password: str) -> str:
    """Hash a password using bcrypt with configured work factor.

    Args:
        password: Plain text password

    Returns:
        Hashed password string

    Security (FR-004):
        Uses bcrypt with work factor from config (default: 12)
    """
    salt = bcrypt.gensalt(rounds=BCRYPT_WORK_FACTOR)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to compare against

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: int, email: str) -> str:
    """Generate JWT access token for authenticated user.

    Args:
        user_id: User's database ID
        email: User's email address

    Returns:
        JWT token string

    Token Claims:
        - sub: User ID (subject)
        - email: User's email
        - exp: Expiration timestamp
        - iat: Issued at timestamp

    Security (FR-006):
        Uses BETTER_AUTH_SECRET from environment
        Token expires after JWT_EXPIRATION_DAYS (default: 7 days)
    """
    now = datetime.utcnow()
    expiration = now + timedelta(days=JWT_EXPIRATION_DAYS)

    payload = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,
        "exp": expiration,  # Expiration time
        "iat": now,  # Issued at time
    }

    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_token(token: str) -> dict:
    """Validate and decode JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload with user_id and email

    Raises:
        UnauthorizedException: If token is invalid, expired, or malformed

    Security (FR-007, FR-008):
        Validates signature using BETTER_AUTH_SECRET
        Checks expiration timestamp
        Rejects tampered tokens
    """
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Token has expired")
    except jwt.InvalidTokenError as e:
        raise UnauthorizedException(f"Invalid token: {str(e)}")


def decode_token(token: str) -> dict:
    """Decode JWT token without verification (for debugging only).

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Warning:
        This does NOT validate the token signature or expiration.
        Only use for debugging. For authentication, use verify_token().
    """
    return jwt.decode(token, options={"verify_signature": False})


def extract_user_id(token: str) -> int:
    """Extract user ID from verified JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID as integer

    Raises:
        UnauthorizedException: If token is invalid

    Security (FR-009):
        Always extracts user_id from JWT token, never trusts client-provided IDs
    """
    payload = verify_token(token)
    user_id = int(payload.get("sub"))
    return user_id


def register_user(email: str, password: str, session: Session) -> User:
    """Register a new user account.

    Args:
        email: User's email address (must be unique)
        password: Plain text password (will be hashed)
        session: Database session

    Returns:
        Created User instance

    Raises:
        DuplicateEmailException: If email already exists

    Business Rules (FR-001, FR-002, FR-003, FR-004):
        - Email must be unique (checked before creation)
        - Email format validated by Pydantic schema
        - Password validation (min 8 chars, letter + number) in schema
        - Password hashed with bcrypt before storage
    """
    # Check for duplicate email (case-insensitive)
    existing_user = session.exec(
        select(User).where(User.email == email.lower())
    ).first()

    if existing_user:
        raise DuplicateEmailException(
            f"Email {email} is already registered",
            details={"email": email}
        )

    # Hash password
    password_hash = hash_password(password)

    # Create user
    user = User(
        email=email.lower(),  # Store email as lowercase
        password_hash=password_hash,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def login_user(email: str, password: str, session: Session) -> tuple[User, str]:
    """Authenticate user and generate JWT token.

    Args:
        email: User's email address
        password: Plain text password
        session: Database session

    Returns:
        Tuple of (User instance, JWT token)

    Raises:
        InvalidCredentialsException: If email doesn't exist or password is incorrect

    Business Rules (FR-005, FR-006):
        - Lookup user by email (case-insensitive)
        - Verify password against stored hash
        - Generate JWT token on successful authentication
    """
    # Lookup user by email (case-insensitive)
    user = session.exec(
        select(User).where(User.email == email.lower())
    ).first()

    # User not found or password incorrect
    # Use same error message for both to prevent email enumeration
    if not user or not verify_password(password, user.password_hash):
        raise InvalidCredentialsException(
            "Invalid email or password",
            details={"email": email}
        )

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    return user, token
