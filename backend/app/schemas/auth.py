"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class RegisterRequest(BaseModel):
    """Request model for user registration."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets security requirements.

        Requirements (FR-003):
        - Minimum 8 characters
        - At least one letter (A-Z or a-z)
        - At least one number (0-9)
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r"[a-zA-Z]", v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one number")
        return v


class LoginRequest(BaseModel):
    """Request model for user login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response model for successful authentication."""

    success: bool = True
    data: dict = Field(
        default_factory=lambda: {
            "message": "Authenticated successfully",
            "token": "jwt_token_here",
        }
    )
    error: Optional[dict] = None


class UserResponse(BaseModel):
    """Public user data (never includes password_hash)."""

    id: int
    email: str
    created_at: str

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility
