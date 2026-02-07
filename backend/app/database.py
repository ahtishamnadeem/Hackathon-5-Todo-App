"""Database connection and session management."""

from sqlmodel import create_engine, Session, SQLModel
from app.config import DATABASE_URL

# Create database engine
# echo=True enables SQL query logging (disable in production)
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for development SQL debugging
    pool_pre_ping=True,  # Verify connections before using from pool
)


def create_db_and_tables():
    """Create all database tables.

    This is useful for development/testing but in production
    use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency for database sessions.

    Usage in endpoints:
        @router.get("/")
        def read_items(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        yield session
