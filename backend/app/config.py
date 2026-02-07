"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Authentication
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_DAYS: int = int(os.getenv("JWT_EXPIRATION_DAYS", "7"))

    # Password Hashing
    BCRYPT_WORK_FACTOR: int = int(os.getenv("BCRYPT_WORK_FACTOR", "12"))

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    def validate(self) -> None:
        """Validate that required settings are present."""
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")
        if not self.BETTER_AUTH_SECRET or len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError(
                "BETTER_AUTH_SECRET must be at least 32 characters. "
                "Generate with: python -c 'import secrets; print(secrets.token_hex(32))'"
            )


# Global settings instance
settings = Settings()

# Export for convenience
DATABASE_URL = settings.DATABASE_URL
BETTER_AUTH_SECRET = settings.BETTER_AUTH_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXPIRATION_DAYS = settings.JWT_EXPIRATION_DAYS
BCRYPT_WORK_FACTOR = settings.BCRYPT_WORK_FACTOR
HOST = settings.HOST
PORT = settings.PORT
FRONTEND_URL = settings.FRONTEND_URL
