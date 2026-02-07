# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2026-01-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase I in-memory console Todo application into a secure, multi-user, production-ready full-stack web application with JWT-based authentication, RESTful API backend, modern frontend, and persistent PostgreSQL storage. The system enforces strict user isolation ensuring each user can only access their own todos, implements comprehensive input validation and error handling, and follows REST API conventions with proper HTTP status codes.

**Core Requirements**: User registration/authentication (FR-001 to FR-011), todo CRUD operations (FR-012 to FR-021), data persistence with user isolation (FR-022 to FR-026), REST API contracts (FR-027 to FR-031), and modern web frontend (FR-032 to FR-038).

**Technical Approach**: Stateless FastAPI backend with JWT middleware for authentication, SQLModel ORM with user-scoped queries, Neon PostgreSQL for persistence, Next.js 16+ frontend with App Router and Better Auth integration, httpOnly cookies for secure token storage.

## Technical Context

**Language/Version**:
- Backend: Python 3.13+
- Frontend: JavaScript/TypeScript with Node.js 20+

**Primary Dependencies**:
- Backend: FastAPI 0.115+, SQLModel 0.0.22+, PyJWT 2.9+, bcrypt 4.2+, psycopg2-binary 2.9+, python-dotenv 1.0+
- Frontend: Next.js 16+, Better Auth (latest), React 19+, TypeScript 5+

**Storage**:
- Database: Neon Serverless PostgreSQL (managed cloud database)
- Session: httpOnly cookies for JWT token storage (frontend)

**Testing**:
- Backend: pytest 8.3+, httpx 0.27+ (for FastAPI test client)
- Frontend: Vitest or Jest for unit tests, Playwright for E2E tests

**Target Platform**:
- Backend: Linux/macOS/Windows server environment (development and production)
- Frontend: Modern web browsers (Chrome, Firefox, Safari, Edge)
- Deployment: Local development initially, cloud-ready architecture

**Project Type**: Web application (requires backend + frontend separation)

**Performance Goals**:
- API response time: <500ms for typical operations (SC-004)
- Todo creation latency: <2 seconds end-to-end (SC-002)
- Support 1000+ todos per user without degradation
- Concurrent multi-user operations without conflicts (SC-008)

**Constraints**:
- Security: Zero data leakage between users (SC-003)
- Authentication: 100% rejection of invalid/expired tokens (SC-006)
- Availability: Graceful degradation on database failures (SC-009)
- Usability: 95% success rate for all operations (SC-005)
- Session persistence: Maintain login across browser restarts (SC-007)

**Scale/Scope**:
- Expected users: 10-100 concurrent users initially
- Data volume: Up to 1000 todos per user
- API endpoints: 8 total (2 auth + 6 todo operations)
- Frontend pages: 3 (login, register, todo dashboard)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Simplicity First, Scalability Later
✅ **PASS**: Architecture uses standard patterns (REST API, JWT auth, CRUD operations) without premature optimization. No caching layer, no microservices, no event sourcing. Simple client-server model with direct database queries through ORM.

### Principle II: Clear Separation of Concerns
✅ **PASS**: Strict boundaries maintained:
- **Frontend**: UI rendering, user interaction, Better Auth integration
- **Backend API**: Business logic, authentication middleware, data validation
- **Database**: Persistent storage via SQLModel ORM
- **Auth Layer**: JWT token generation/validation isolated in middleware

### Principle III: Spec-Driven Development
✅ **PASS**: All 38 functional requirements (FR-001 to FR-038) from spec.md are directly mapped to implementation phases. Each requirement is testable and traceable. Success criteria (SC-001 to SC-010) provide measurable validation.

### Principle IV: Determinism Before Augmentation
✅ **PASS**: No AI features in Phase II. All business logic is deterministic (create todo, update todo, delete todo). Authentication and authorization follow standard JWT patterns.

### Principle V: Developer-Friendly and Testable
✅ **PASS**:
- FastAPI provides automatic OpenAPI documentation
- SQLModel offers type-safe database operations
- Each API endpoint independently testable via pytest
- Frontend components testable via unit and E2E tests
- Clear project structure with separation of models, services, API routes

### Principle VI: Security-First Architecture
✅ **PASS**:
- JWT authentication required on all protected endpoints (FR-007, FR-008)
- User-scoped database queries prevent data leakage (FR-023, FR-026)
- Password hashing with bcrypt/argon2 (FR-004)
- httpOnly cookies prevent XSS token theft (FR-010)
- Input validation on all endpoints (FR-030)
- SQL injection prevention via SQLModel parameterized queries

### Principle VII: Correctness by Design
✅ **PASS**: Implementation plan maps directly to spec requirements. Each functional requirement (FR-001 to FR-038) will have corresponding code and tests. Acceptance scenarios from user stories provide explicit test cases.

### Principle VIII: Production Readiness
✅ **PASS**:
- Proper HTTP status codes (200, 201, 400, 401, 404, 500) per FR-028
- Structured error responses with codes and messages (FR-029)
- Input validation using Pydantic models (FR-030)
- Graceful error handling for database failures (SC-009)
- Stateless backend enables horizontal scaling
- Environment-based configuration (no hardcoded secrets)

### Phase II Specific Requirements
✅ **PASS**:
- **JWT Authentication**: All API endpoints except auth routes require valid JWT (FR-007, FR-008)
- **User Isolation**: All queries scoped to authenticated user (FR-023, FR-026)
- **Stateless Backend**: No server-side sessions, JWT carries user identity
- **REST Standards**: Standard HTTP methods and status codes (FR-027, FR-028)
- **Better Auth Integration**: Frontend uses Better Auth for user management
- **Neon PostgreSQL**: Managed database with automatic backups

**Result**: ALL GATES PASSED ✅ - Ready for Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── openapi.yaml     # Full OpenAPI 3.0 specification
│   ├── auth.md          # Authentication flow documentation
│   └── errors.md        # Error response specifications
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                 # Python FastAPI application
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── config.py        # Environment configuration (DATABASE_URL, SECRET_KEY)
│   ├── database.py      # Database connection and session management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py      # User SQLModel (id, email, password_hash, timestamps)
│   │   └── todo.py      # Todo SQLModel (id, user_id, title, description, completed, timestamps)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py      # Auth request/response models (RegisterRequest, LoginRequest, TokenResponse)
│   │   └── todo.py      # Todo request/response models (TodoCreate, TodoUpdate, TodoResponse)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py      # Authentication service (password hashing, JWT generation/validation)
│   │   └── todo.py      # Todo business logic (CRUD operations with user scoping)
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py      # JWT authentication middleware (extract/verify token, decode user_id)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py      # Auth endpoints (/register, /login, /logout)
│   │   └── todos.py     # Todo endpoints (GET /todos, POST /todos, PATCH /todos/{id}, DELETE /todos/{id})
│   └── utils/
│       ├── __init__.py
│       ├── errors.py    # Custom exception classes and error handlers
│       └── validators.py # Input validation helpers
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # pytest fixtures (test client, test database)
│   ├── test_auth.py     # Authentication endpoint tests
│   ├── test_todos.py    # Todo CRUD endpoint tests
│   └── test_isolation.py # Multi-user isolation tests
├── alembic/             # Database migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Python project metadata
└── .env.example         # Environment variable template

frontend/                # Next.js 16+ application
├── src/
│   ├── app/             # App Router
│   │   ├── layout.tsx   # Root layout
│   │   ├── page.tsx     # Landing/redirect page
│   │   ├── login/
│   │   │   └── page.tsx # Login page
│   │   ├── register/
│   │   │   └── page.tsx # Registration page
│   │   └── dashboard/
│   │       └── page.tsx # Todo dashboard (protected route)
│   ├── components/
│   │   ├── TodoList.tsx   # Todo list display
│   │   ├── TodoItem.tsx   # Individual todo item with actions
│   │   ├── CreateTodoForm.tsx # Form for creating new todos
│   │   ├── EditTodoForm.tsx   # Form for editing todos
│   │   └── AuthGuard.tsx      # Protected route wrapper
│   ├── lib/
│   │   ├── api.ts       # API client with JWT token injection
│   │   ├── auth.ts      # Better Auth configuration
│   │   └── types.ts     # TypeScript type definitions
│   └── hooks/
│       ├── useTodos.ts  # Custom hook for todo operations
│       └── useAuth.ts   # Custom hook for authentication state
├── public/
├── tests/
│   ├── unit/            # Component unit tests
│   └── e2e/             # Playwright E2E tests
├── package.json
├── tsconfig.json
├── next.config.js
└── .env.local.example   # Environment variable template

.github/
└── workflows/           # CI/CD pipelines (optional for hackathon)

docs/
├── api.md               # API endpoint documentation
├── authentication.md    # Authentication flow guide
└── deployment.md        # Deployment instructions
```

**Structure Decision**: Selected **Web Application** structure (Option 2) due to frontend + backend requirement. Backend is Python FastAPI (stateless REST API), frontend is Next.js 16+ (App Router). Clear separation enables independent development and testing of each tier. Backend follows FastAPI best practices with routers, models, schemas, services, and middleware separation. Frontend uses Next.js App Router convention with app directory, components, and lib utilities.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All constitution principles passed. This section is not applicable.*

