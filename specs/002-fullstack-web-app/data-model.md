# Data Model Specification

**Feature**: Todo Full-Stack Web Application (Phase II)
**Date**: 2026-01-08
**Database**: PostgreSQL (Neon Serverless)
**ORM**: SQLModel 0.0.22+

## Overview

This document defines the complete data model for Phase II, including database schema, entity relationships, validation rules, and state transitions. All models are implemented using SQLModel (combining Pydantic and SQLAlchemy) for type-safe database operations and automatic API validation.

## Entity Relationship Diagram

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │◄──────┐
│ email (UNIQUE)  │       │ 1
│ password_hash   │       │
│ created_at      │       │
│ updated_at      │       │
└─────────────────┘       │
                          │
                          │ user_id (FK)
                          │ ON DELETE CASCADE
                          │
┌─────────────────┐       │
│      Todo       │       │
├─────────────────┤       │
│ id (PK)         │       │
│ user_id (FK) ───┼───────┘ *
│ title           │
│ description     │
│ completed       │
│ created_at      │
│ updated_at      │
└─────────────────┘

Relationship: User 1:* Todo (One user has many todos)
```

## Entities

### 1. User Entity

**Purpose**: Represents a registered user account with authentication credentials.

**Source**: FR-001, FR-002, FR-003, FR-004, FR-005

#### Fields

| Field          | Type         | Constraints                    | Description                                      |
|----------------|--------------|--------------------------------|--------------------------------------------------|
| id             | Integer      | Primary Key, Auto-increment    | Unique user identifier                           |
| email          | String(255)  | Unique, Not Null, Email format | User's email address for login                   |
| password_hash  | String(255)  | Not Null                       | Bcrypt hashed password (never store plaintext)   |
| created_at     | DateTime     | Not Null, Default NOW()        | Account creation timestamp                       |
| updated_at     | DateTime     | Not Null, Default NOW()        | Last account update timestamp                    |

#### Validation Rules

- **email**:
  - MUST be valid email format (regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
  - MUST be unique across all users (database constraint + unique index)
  - Case-insensitive comparison (store as lowercase)
  - Required during registration (FR-002)

- **password** (before hashing):
  - MUST be at least 8 characters (FR-003)
  - MUST contain at least one letter (A-Z or a-z)
  - MUST contain at least one number (0-9)
  - Hashed using bcrypt with work factor 12 before storage (FR-004)

#### Database Indexes

```sql
CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));
```

#### Relationships

- **Todos**: One-to-many relationship with Todo entity (one user has many todos)
  - Cascade delete: When user is deleted, all their todos are automatically deleted (FR-025)

#### State Transitions

User entity has minimal state (account exists or doesn't exist):

```
[Non-existent] --[Register]--> [Active]
[Active] --[Delete Account]--> [Deleted]
```

---

### 2. Todo Entity

**Purpose**: Represents a single task item owned by a user.

**Source**: FR-012, FR-013, FR-016, FR-017, FR-019, FR-020

#### Fields

| Field          | Type         | Constraints                    | Description                                      |
|----------------|--------------|--------------------------------|--------------------------------------------------|
| id             | Integer      | Primary Key, Auto-increment    | Unique todo identifier                           |
| user_id        | Integer      | Foreign Key, Not Null, Index   | References users.id (owner of this todo)         |
| title          | String(500)  | Not Null                       | Todo title/summary                               |
| description    | Text         | Nullable                       | Optional detailed description                    |
| completed      | Boolean      | Not Null, Default False        | Completion status (true = done, false = pending) |
| created_at     | DateTime     | Not Null, Default NOW()        | Todo creation timestamp                          |
| updated_at     | DateTime     | Not Null, Default NOW()        | Last todo update timestamp                       |

#### Validation Rules

- **user_id**:
  - MUST reference valid user (foreign key constraint)
  - MUST be extracted from authenticated JWT token (never from request body) (FR-009, FR-014)
  - Cannot be null or changed after creation

- **title**:
  - MUST be non-empty after trimming whitespace (FR-013)
  - Maximum length: 500 characters
  - Required field (cannot be null or empty string)

- **description**:
  - Optional field (can be null or empty)
  - Maximum length: 10,000 characters (prevents abuse)
  - Defaults to null if not provided

- **completed**:
  - Boolean value (true or false)
  - Defaults to false (new todos are incomplete)
  - Can be toggled via PATCH endpoint (FR-019)

#### Database Indexes

```sql
-- Performance index for user_id queries (most common access pattern)
CREATE INDEX idx_todos_user_id ON todos(user_id);

-- Composite index for user_id + created_at (supports default sort)
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);
```

#### Relationships

- **User**: Many-to-one relationship with User entity (many todos belong to one user)
  - Foreign key: user_id REFERENCES users(id) ON DELETE CASCADE
  - Indexed for performance (all queries filter by user_id)

#### State Transitions

Todo entity has two primary states: incomplete and completed.

```
[Non-existent] --[Create]--> [Incomplete]
[Incomplete] --[Toggle Complete]--> [Completed]
[Completed] --[Toggle Complete]--> [Incomplete]
[Incomplete/Completed] --[Update]--> [Incomplete/Completed] (same state, different data)
[Incomplete/Completed] --[Delete]--> [Deleted]
```

**State Machine Rules**:
- New todos start in **Incomplete** state (completed = false)
- Toggling completion flips the boolean (incomplete ↔ completed)
- Updating title/description does NOT change completion state
- Deletion is permanent (no soft delete in Phase II)

---

## SQLModel Definitions

### User Model (backend/app/models/user.py)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """Database model for User entity."""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }
```

### Todo Model (backend/app/models/todo.py)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Todo(SQLModel, table=True):
    """Database model for Todo entity."""
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": false,
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }
```

---

## API Request/Response Schemas

### Authentication Schemas (backend/app/schemas/auth.py)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RegisterRequest(BaseModel):
    """Request model for user registration."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)

class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    """Response model for successful authentication."""
    success: bool = True
    data: dict = Field(default_factory=lambda: {"message": "Authenticated successfully"})
    error: Optional[dict] = None

class UserResponse(BaseModel):
    """Public user data (never includes password_hash)."""
    id: int
    email: str
    created_at: str
```

### Todo Schemas (backend/app/schemas/todo.py)

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    """Request model for creating a new todo."""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)

class TodoUpdate(BaseModel):
    """Request model for updating a todo (all fields optional for PATCH)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    """Response model for todo data."""
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode

class TodoListResponse(BaseModel):
    """Response model for list of todos."""
    success: bool = True
    data: list[TodoResponse]
    error: Optional[dict] = None
```

---

## Database Migrations

### Initial Migration (Alembic)

**Migration**: `001_create_users_and_todos_tables`

```sql
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Create unique index on lowercase email
CREATE UNIQUE INDEX idx_users_email ON users(LOWER(email));

-- Create todos table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_todos_user FOREIGN KEY (user_id)
        REFERENCES users(id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);
```

---

## Data Access Patterns

### User Isolation Queries (Critical Security Requirement)

All todo queries MUST be scoped to the authenticated user to prevent data leakage (FR-023, FR-026).

**✅ CORRECT: User-scoped query**
```python
def get_user_todos(user_id: int, db: Session) -> list[Todo]:
    """Get all todos for authenticated user (SECURE)."""
    return db.query(Todo).filter(Todo.user_id == user_id).all()
```

**❌ INCORRECT: Unscoped query (SECURITY VULNERABILITY)**
```python
def get_all_todos(db: Session) -> list[Todo]:
    """Get ALL todos (INSECURE - violates FR-026)."""
    return db.query(Todo).all()  # NEVER DO THIS
```

### Default Sort Order

Todos MUST be ordered by creation date with newest first (FR-017).

```python
def get_user_todos(user_id: int, db: Session) -> list[Todo]:
    """Get user todos ordered by created_at DESC."""
    return (
        db.query(Todo)
        .filter(Todo.user_id == user_id)
        .order_by(Todo.created_at.desc())
        .all()
    )
```

### Update Operations with User Verification

Updates and deletes MUST verify ownership before modifying data (FR-021).

```python
def update_todo(todo_id: int, user_id: int, data: TodoUpdate, db: Session) -> Optional[Todo]:
    """Update todo only if owned by user (SECURE)."""
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id  # Critical security check
    ).first()

    if not todo:
        return None  # Will return 404 Not Found

    # Update fields
    if data.title is not None:
        todo.title = data.title
    if data.description is not None:
        todo.description = data.description
    if data.completed is not None:
        todo.completed = data.completed

    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo
```

---

## Edge Cases & Constraints

### Concurrent Modifications

**Scenario**: User has app open in two browser tabs and updates the same todo simultaneously.

**Resolution**: Last write wins (optimistic locking not required for Phase II). The `updated_at` timestamp reflects the most recent update.

### Database Connection Failures

**Scenario**: Neon database becomes temporarily unavailable during operation.

**Resolution**: FastAPI raises HTTP 500 Internal Server Error with user-friendly message (SC-009). Frontend displays error toast and allows retry.

### Cascade Delete

**Scenario**: User account is deleted.

**Resolution**: All user's todos are automatically deleted via `ON DELETE CASCADE` foreign key constraint (FR-025). This is handled at the database level.

### Empty Title Submission

**Scenario**: User submits todo with empty or whitespace-only title.

**Resolution**: Pydantic validation rejects with 400 Bad Request before reaching database (FR-013).

### Extremely Long Inputs

**Scenario**: User submits title >500 characters or description >10,000 characters.

**Resolution**: Pydantic validation rejects with 400 Bad Request and detailed error message.

---

## Summary

**Entities Defined**: 2 (User, Todo)
**Relationships**: 1 (User 1:* Todo with cascade delete)
**Database Tables**: 2 (users, todos)
**Indexes**: 3 (users.email unique, todos.user_id, todos.user_id+created_at)
**API Schemas**: 7 (RegisterRequest, LoginRequest, TokenResponse, UserResponse, TodoCreate, TodoUpdate, TodoResponse)

**Security Requirements Met**:
- ✅ User isolation via user_id scoping (FR-023, FR-026)
- ✅ Password hashing (never store plaintext) (FR-004)
- ✅ Foreign key constraints for referential integrity (FR-024)
- ✅ Cascade delete for data cleanup (FR-025)
- ✅ Input validation at schema level (FR-030)

**Status**: Data model complete and ready for API contract generation ✅
