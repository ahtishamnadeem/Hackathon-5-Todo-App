import asyncio
from sqlmodel import SQLModel, create_engine
from app.models.user import User
from app.models.todo import Todo
from app.models.conversation import Conversation
from app.models.message import Message
from app.database import DATABASE_URL

# Create the database engine
engine = create_engine(DATABASE_URL)

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")

    # Create all tables defined in SQLModel metadata
    SQLModel.metadata.create_all(engine)

    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()