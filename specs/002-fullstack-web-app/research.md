# Research & Technical Decisions

**Feature**: Todo Full-Stack Web Application (Phase II)
**Date**: 2026-01-08
**Status**: Complete

## Overview

This document captures all technical research and decision-making for Phase II implementation. All decisions are guided by the constitution v2.0.0 principles (security-first, correctness by design, production readiness) and the 38 functional requirements from spec.md.

## 1. Backend Framework: FastAPI

### Decision
Use **FastAPI 0.115+** as the Python backend framework.

### Rationale
- **Automatic API Documentation**: Built-in OpenAPI/Swagger generation (satisfies FR-027 REST API requirement)
- **Type Safety**: Pydantic integration provides automatic request/response validation (FR-030)
- **Performance**: ASGI-based, async support enables <500ms response times (SC-004)
- **Developer Experience**: Type hints enable IDE autocompletion and early error detection
- **Mature Ecosystem**: Well-established patterns for JWT middleware and database integration

### Alternatives Considered
- **Django REST Framework**: More batteries-included but heavier weight, slower startup, less type-safe
- **Flask**: Simpler but requires more manual setup for async, validation, and documentation
- **Rejected**: Both alternatives don't provide the same level of automatic validation and documentation

### Best Practices
- Use dependency injection for database sessions
- Separate routers by domain (auth, todos)
- Use Pydantic models for all request/response schemas
- Implement custom exception handlers for consistent error responses

## 2. ORM: SQLModel

### Decision
Use **SQLModel 0.0.22+** for database modeling and queries.

### Rationale
- **Type Safety**: Combines Pydantic and SQLAlchemy for full type coverage
- **SQL Injection Prevention**: Parameterized queries by default (FR-026 security requirement)
- **Simplicity**: Single model definition works for both database schema and API validation
- **FastAPI Integration**: Seamless integration with FastAPI's dependency injection
- **Maintainability**: Less boilerplate than raw SQLAlchemy, clearer than raw SQL

### Alternatives Considered
- **Raw SQLAlchemy**: More control but more boilerplate, no built-in Pydantic validation
- **Tortoise ORM**: Async-first but less mature, smaller community
- **Rejected**: SQLModel provides the best balance of simplicity and power for this use case

### Best Practices
- Define separate table models (User, Todo) and API schemas (UserCreate, TodoResponse)
- Use relationship() for foreign keys with lazy loading
- Always scope queries with user_id filter for isolation (FR-023)
- Use Alembic for schema migrations

## 3. Authentication: JWT with Better Auth

### Decision
- **Backend**: Use **PyJWT 2.9+** for token generation and validation
- **Frontend**: Use **Better Auth** for user management and JWT issuance
- **Token Storage**: httpOnly cookies (not localStorage)

### Rationale
- **Stateless**: JWT enables horizontal scaling without session stores (Constitution Principle VIII)
- **Security**: httpOnly cookies prevent XSS attacks (FR-010)
- **Shared Secret**: BETTER_AUTH_SECRET environment variable enables backend JWT validation
- **Simplicity**: No need for session database or Redis
- **Standard**: JWT is industry standard with mature libraries

### Better Auth Integration Pattern
```text
Frontend (Better Auth) → Issues JWT with user_id claim
Backend (PyJWT) → Validates JWT signature using BETTER_AUTH_SECRET
Backend → Extracts user_id from token payload for database scoping
```

### Alternatives Considered
- **Session-based auth**: Requires Redis/database for session storage, not stateless
- **OAuth2 Password Flow**: More complex, overkill for simple email/password auth
- **Rejected**: JWT with Better Auth provides simplest path to secure, stateless authentication

### Best Practices
- JWT payload: `{"user_id": <id>, "email": "<email>", "exp": <timestamp>}`
- Token expiration: 7 days (configurable)
- Middleware extracts user_id and injects into request context
- All protected routes require valid JWT (401 Unauthorized if missing/invalid)

## 4. Database: Neon Serverless PostgreSQL

### Decision
Use **Neon Serverless PostgreSQL** as the managed database service.

### Rationale
- **Managed Service**: Automatic backups, high availability (assumption from spec)
- **PostgreSQL Compatibility**: Full SQL support with referential integrity (FR-024)
- **Serverless**: Auto-scaling, pay-per-use model
- **Developer Experience**: Simple connection string configuration
- **Production-Ready**: Battle-tested PostgreSQL engine

### Schema Design
```sql
-- User table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Todo table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
```

### Alternatives Considered
- **SQLite**: Simple but not suitable for multi-user production deployment
- **MySQL**: Viable but PostgreSQL has better JSON support and more features
- **MongoDB**: NoSQL doesn't provide referential integrity (FR-024 requirement)
- **Rejected**: PostgreSQL via Neon provides best balance of features and ease of use

### Best Practices
- Use Alembic for migrations (version-controlled schema changes)
- Cascade delete on user deletion (FR-025)
- Index on user_id foreign key for query performance
- Connection pooling via SQLAlchemy engine

## 5. Frontend Framework: Next.js 16+ (App Router)

### Decision
Use **Next.js 16+** with App Router, React Server Components, and TypeScript.

### Rationale
- **Modern React**: App Router with React Server Components provides better performance
- **Type Safety**: TypeScript integration prevents runtime errors (FR-037 error handling)
- **Developer Experience**: File-based routing, built-in optimization
- **Production-Ready**: Automatic code splitting, image optimization, SEO support
- **Better Auth Support**: Official Better Auth integration available

### Alternatives Considered
- **Create React App**: No longer recommended, lacks modern features
- **Vite + React**: Faster dev server but lacks Next.js server-side features
- **Remix**: Good alternative but smaller ecosystem
- **Rejected**: Next.js is the most mature and feature-complete React framework

### Best Practices
- Use App Router (not Pages Router)
- Client Components for interactive UI (forms, buttons)
- Server Components for static content where possible
- Custom hooks for API calls (useTodos, useAuth)
- Centralized API client with token injection

## 6. Password Hashing: bcrypt

### Decision
Use **bcrypt 4.2+** for password hashing.

### Rationale
- **Security**: Industry-standard algorithm with salt generation (FR-004)
- **Adaptive**: Work factor can be increased as hardware improves
- **Battle-Tested**: 20+ years of cryptographic analysis
- **Python Support**: Mature py-bcrypt library

### Alternatives Considered
- **argon2**: Newer, more resistant to GPU attacks, but bcrypt is simpler and sufficient for this use case
- **PBKDF2**: Older, less secure than bcrypt
- **Rejected**: bcrypt provides the best balance of security and simplicity

### Best Practices
- Use work factor 12 (good balance of security and performance)
- Never store plaintext passwords
- Use bcrypt.hashpw() for hashing during registration
- Use bcrypt.checkpw() for validation during login

## 7. Input Validation Strategy

### Decision
- **Backend**: Pydantic models for automatic validation (FR-030)
- **Frontend**: HTML5 validation + client-side checks for UX

### Rationale
- **Backend Validation is Source of Truth**: Never trust client input (Constitution Principle VI)
- **Client Validation is UX Enhancement**: Provides immediate feedback (SC-005 95% success rate)
- **Type Safety**: Pydantic integrates with FastAPI for automatic request validation

### Validation Rules
- **Email**: Regex pattern for valid email format (FR-002)
- **Password**: Min 8 characters, at least one letter and one number (FR-003)
- **Todo Title**: Non-empty after trim, max 500 characters (FR-013)
- **Todo Description**: Optional, max 10,000 characters (edge case handling)

### Best Practices
- Return 400 Bad Request with detailed error messages on validation failure (FR-031)
- Use Pydantic Field() with constraints (min_length, max_length, regex)
- Frontend shows validation errors inline with form fields

## 8. Error Handling Architecture

### Decision
Standardized error response format across all endpoints (FR-029).

### Error Response Schema
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}  // Optional field-specific details
  }
}
```

### HTTP Status Code Mapping (FR-028)
- **200 OK**: Successful GET, PATCH, DELETE
- **201 Created**: Successful POST (new resource created)
- **400 Bad Request**: Validation errors, malformed input
- **401 Unauthorized**: Missing, invalid, or expired JWT token
- **404 Not Found**: Resource doesn't exist or user lacks access
- **500 Internal Server Error**: Unexpected server errors

### Rationale
- **Consistency**: Same format for all errors simplifies frontend error handling
- **Debugging**: Error codes enable precise error identification
- **Security**: 404 for unauthorized access prevents information leakage (not 403)

### Best Practices
- Define custom exception classes (UnauthorizedException, ValidationException)
- Use FastAPI exception handlers to catch and format all exceptions
- Log 500 errors with stack traces for debugging
- Never expose internal error details to clients

## 9. User Isolation Strategy

### Decision
**Middleware-enforced user scoping** on all database queries (FR-023, FR-026).

### Implementation Pattern
```python
# Middleware extracts user_id from JWT
def get_current_user(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY)
    return payload["user_id"]

# All todo queries scoped to authenticated user
def get_todos(user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def update_todo(todo_id: int, user_id: int, data: TodoUpdate):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == user_id  # Critical security check
    ).first()
    if not todo:
        raise NotFoundException()  # Returns 404, not 403
```

### Rationale
- **Defense in Depth**: User isolation enforced at multiple layers (middleware, query, business logic)
- **Zero Trust**: Never trust client-provided user IDs (FR-009)
- **Information Hiding**: Return 404 instead of 403 to prevent user enumeration

### Best Practices
- Always filter by user_id in WHERE clauses
- Never allow user_id in request bodies (extract from JWT only)
- Test isolation with multi-user scenarios (test_isolation.py)
- Return 404 for unauthorized access attempts (not 403)

## 10. Testing Strategy

### Decision
- **Backend**: pytest with TestClient for API endpoint testing
- **Frontend**: Vitest for unit tests, Playwright for E2E tests

### Test Coverage Requirements
- **Unit Tests**: All services, models, utilities
- **Integration Tests**: All API endpoints with authentication
- **Isolation Tests**: Multi-user scenarios verifying zero data leakage (SC-003)
- **E2E Tests**: Complete user flows (register → login → CRUD operations)

### Rationale
- **Confidence**: Comprehensive testing ensures correctness (Constitution Principle VII)
- **Regression Prevention**: Tests catch breaking changes early
- **Documentation**: Tests serve as executable specifications

### Best Practices
- Use pytest fixtures for test database and client setup
- Test both success and failure cases for each endpoint
- Mock external dependencies (Neon database in CI)
- Achieve >80% code coverage

## 11. Environment Configuration

### Decision
Use **environment variables** for all configuration (no hardcoded secrets).

### Required Environment Variables
**Backend (.env)**
```bash
DATABASE_URL=postgresql://user:pass@neon-host/dbname
BETTER_AUTH_SECRET=shared-secret-with-frontend
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
BCRYPT_WORK_FACTOR=12
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=shared-secret-with-backend
```

### Rationale
- **Security**: No secrets in code or version control (Constitution Principle VI)
- **Flexibility**: Easy configuration for dev/staging/prod environments
- **Best Practice**: 12-factor app methodology

### Best Practices
- Provide .env.example templates (never commit .env)
- Use python-dotenv for backend config loading
- Validate required env vars at startup (fail fast if missing)
- Use NEXT_PUBLIC_ prefix for client-side Next.js vars

## 12. API Endpoint Design

### Decision
RESTful API following standard HTTP semantics (FR-027).

### Endpoint Specification
**Authentication Endpoints** (Unauthenticated)
- `POST /api/auth/register` - Create new user account
- `POST /api/auth/login` - Authenticate and receive JWT token
- `POST /api/auth/logout` - Terminate session (clear cookie)

**Todo Endpoints** (Authenticated)
- `GET /api/todos` - List all user's todos
- `POST /api/todos` - Create new todo
- `GET /api/todos/{id}` - Get single todo (if owned by user)
- `PATCH /api/todos/{id}` - Update todo (title, description, or completed)
- `DELETE /api/todos/{id}` - Delete todo permanently

### Rationale
- **RESTful**: Standard HTTP methods (GET, POST, PATCH, DELETE)
- **Idempotent**: GET, PATCH, DELETE are idempotent (safe to retry)
- **Discoverable**: OpenAPI documentation auto-generated by FastAPI

### Best Practices
- Use plural nouns for resources (/todos, not /todo)
- Use PATCH for partial updates (not PUT for full replacement)
- Return 201 Created with Location header for POST
- Include resource in response body for all mutations

## Summary

All technical decisions are **complete and unambiguous**. No additional research required. Key decisions:

1. ✅ **Backend**: FastAPI 0.115+ with SQLModel 0.0.22+ and PyJWT 2.9+
2. ✅ **Frontend**: Next.js 16+ with TypeScript and Better Auth
3. ✅ **Database**: Neon Serverless PostgreSQL with Alembic migrations
4. ✅ **Authentication**: JWT tokens in httpOnly cookies, validated via shared secret
5. ✅ **Security**: User-scoped queries, bcrypt password hashing, input validation
6. ✅ **Error Handling**: Standardized JSON format with proper HTTP status codes
7. ✅ **Testing**: pytest for backend, Vitest/Playwright for frontend
8. ✅ **Configuration**: Environment variables for all secrets and config

All decisions align with constitution v2.0.0 principles and satisfy all 38 functional requirements from spec.md.

**Status**: Ready for Phase 1 (Data Model & Contracts) ✅
