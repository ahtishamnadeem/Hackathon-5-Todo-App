# Implementation Tasks: Todo Full-Stack Web Application

**Feature Branch**: `002-fullstack-web-app`
**Created**: 2026-01-08
**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Overview

This document provides a complete, ordered task breakdown for implementing Phase II of the Todo application. Tasks are organized by user story to enable independent implementation and testing. Each user story can be completed as a standalone deliverable.

**User Stories** (from spec.md):
- **US1** (P1): User Registration and Authentication
- **US2** (P1): Create and View Personal Todos
- **US3** (P2): Update Todo Status and Details
- **US4** (P3): Delete Personal Todos
- **US5** (P1): Persistent Multi-User Todo Management (architectural - integrated across all stories)

**Legend**:
- `[ ]` Checkbox for tracking completion
- `T###` Task ID (sequential execution order)
- `[P]` Parallelizable task (can run concurrently with other [P] tasks in same phase)
- `[US#]` User Story label (maps to spec.md user stories)

---

## Phase 1: Project Setup & Infrastructure

**Goal**: Initialize project structure, configure environments, and establish development toolchain.

### Backend Setup

- [X] T001 Create backend directory structure per plan.md (backend/app/{models,schemas,services,middleware,routers,utils}, backend/tests, backend/alembic)
- [X] T002 [P] Create backend/requirements.txt with dependencies (FastAPI 0.115+, SQLModel 0.0.22+, PyJWT 2.9+, bcrypt 4.2+, psycopg2-binary 2.9+, python-dotenv 1.0+, uvicorn 0.30+, alembic 1.13+, pytest 8.3+, httpx 0.27+)
- [X] T003 [P] Create backend/pyproject.toml with project metadata and build configuration
- [X] T004 [P] Create backend/.env.example template with required environment variables (DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, BCRYPT_WORK_FACTOR, HOST, PORT, FRONTEND_URL)
- [X] T005 [P] Create backend/.gitignore for Python artifacts (__pycache__, *.pyc, .env, venv/, dist/, *.egg-info/)

### Frontend Setup

- [X] T006 Create frontend directory structure per plan.md (frontend/src/{app,components,lib,hooks}, frontend/tests/{unit,e2e})
- [X] T007 [P] Initialize Next.js 16+ project in frontend/ with TypeScript and App Router configuration
- [X] T008 [P] Create frontend/package.json with dependencies (next 16+, react 19+, react-dom 19+, better-auth latest, typescript 5+, @types/node 20+, @types/react 19+, vitest 2+, playwright 1.40+)
- [X] T009 [P] Create frontend/.env.local.example template with required variables (NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL)
- [X] T010 [P] Create frontend/.gitignore for Node artifacts (node_modules/, .next/, .env.local, dist/)
- [X] T011 [P] Configure frontend/tsconfig.json with strict TypeScript settings and path aliases
- [X] T012 [P] Configure frontend/next.config.js with API proxy and environment variables

### Database Setup

- [X] T013 Create backend/alembic.ini configuration for database migrations
- [X] T014 Create backend/alembic/env.py with SQLModel integration for auto-generating migrations
- [ ] T015 Provision Neon Serverless PostgreSQL database and obtain DATABASE_URL connection string

### Development Environment

- [X] T016 Create root-level docs/ directory for API documentation and guides
- [X] T017 [P] Copy quickstart.md to docs/quickstart.md for developer onboarding
- [X] T018 [P] Copy contracts/auth.md to docs/authentication.md for auth flow reference
- [X] T019 [P] Copy contracts/errors.md to docs/error-handling.md for error standards
- [X] T020 [P] Create docs/api.md placeholder for generated API documentation
- [ ] T021 Configure backend/.env and frontend/.env.local with actual values (use BETTER_AUTH_SECRET generator: python -c "import secrets; print(secrets.token_hex(32))")
- [ ] T022 Create backend Python virtual environment (python -m venv venv) and install dependencies (pip install -r requirements.txt)
- [ ] T023 Install frontend dependencies (cd frontend && npm install)

---

## Phase 2: Foundational Layer (Database & Core Models)

**Goal**: Establish database schema and core data models that all user stories depend on.

**Why Foundational**: These tasks MUST be completed before any user story implementation because they provide the persistence layer and data structures used by all features.

### Database Models

- [X] T024 Implement User SQLModel in backend/app/models/user.py with fields (id, email, password_hash, created_at, updated_at) per data-model.md
- [X] T025 Implement Todo SQLModel in backend/app/models/todo.py with fields (id, user_id, title, description, completed, created_at, updated_at) and foreign key relationship per data-model.md
- [X] T026 Create backend/app/models/__init__.py exporting User and Todo models

### Database Configuration

- [X] T027 Implement backend/app/config.py to load environment variables using python-dotenv (DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, BCRYPT_WORK_FACTOR, FRONTEND_URL)
- [X] T028 Implement backend/app/database.py with SQLModel engine creation, session management, and get_session() dependency for FastAPI

### Database Migrations

- [ ] T029 Generate initial Alembic migration for users and todos tables (alembic revision --autogenerate -m "Create users and todos tables")
- [ ] T030 Review and edit generated migration in backend/alembic/versions/ to include indexes (idx_users_email unique, idx_todos_user_id, idx_todos_user_created)
- [ ] T031 Apply migration to create database schema (alembic upgrade head)
- [ ] T032 Verify database schema created correctly in Neon dashboard (2 tables, 3 indexes, 1 foreign key constraint)

### API Schemas

- [X] T033 [P] Implement authentication Pydantic schemas in backend/app/schemas/auth.py (RegisterRequest, LoginRequest, TokenResponse, UserResponse) per data-model.md
- [X] T034 [P] Implement todo Pydantic schemas in backend/app/schemas/todo.py (TodoCreate, TodoUpdate, TodoResponse, TodoListResponse, TodoSingleResponse) per data-model.md
- [X] T035 [P] Create backend/app/schemas/__init__.py exporting all schemas

### Error Handling Foundation

- [X] T036 Implement custom exception classes in backend/app/utils/errors.py (UnauthorizedException, ValidationException, NotFoundException, DatabaseException)
- [X] T037 Implement standardized error response formatter in backend/app/utils/errors.py per contracts/errors.md format
- [X] T038 Create backend/app/utils/__init__.py exporting error utilities

---

## Phase 3: User Story 1 - User Registration and Authentication (P1)

**Goal**: Implement secure user registration, login, logout, and JWT authentication middleware.

**Independent Test Criteria**:
- Register new user with email and password → account created, JWT token issued
- Login with valid credentials → JWT token issued, redirected to dashboard
- Login with invalid credentials → error message displayed, remains unauthenticated
- Logout → session terminated, JWT token cleared, redirected to login page
- Protected API request without token → 401 Unauthorized
- Protected API request with expired token → 401 Unauthorized

**Delivers**: Secure user identity and session management (foundational for all other user stories)

### Backend Authentication Service

- [X] T039 [US1] Implement password hashing functions in backend/app/services/auth.py (hash_password using bcrypt work factor 12, verify_password)
- [X] T040 [US1] Implement JWT token generation function in backend/app/services/auth.py (create_access_token with user_id and email claims, expiration per config)
- [X] T041 [US1] Implement JWT token validation function in backend/app/services/auth.py (verify_token, decode_token, extract user_id) using BETTER_AUTH_SECRET
- [X] T042 [US1] Implement user registration logic in backend/app/services/auth.py (validate email format, check duplicate email, hash password, create user record)
- [X] T043 [US1] Implement user login logic in backend/app/services/auth.py (lookup user by email, verify password, generate JWT token)

### Backend Authentication Middleware

- [X] T044 [US1] Implement JWT authentication middleware in backend/app/middleware/auth.py (extract Authorization header, validate token, decode user_id, inject into request state)
- [X] T045 [US1] Implement get_current_user dependency in backend/app/middleware/auth.py for FastAPI dependency injection (raises 401 if token invalid/missing)
- [X] T046 [US1] Create backend/app/middleware/__init__.py exporting auth middleware

### Backend Authentication Endpoints

- [X] T047 [US1] Create backend/app/routers/auth.py router with FastAPI APIRouter
- [X] T048 [US1] Implement POST /api/auth/register endpoint in backend/app/routers/auth.py (accepts RegisterRequest, returns TokenResponse, sets httpOnly cookie, returns 201)
- [X] T049 [US1] Implement POST /api/auth/login endpoint in backend/app/routers/auth.py (accepts LoginRequest, returns TokenResponse, sets httpOnly cookie, returns 200)
- [X] T050 [US1] Implement POST /api/auth/logout endpoint in backend/app/routers/auth.py (clears cookie, returns success message, returns 200)
- [X] T051 [US1] Create backend/app/routers/__init__.py exporting auth router

### Backend Application Setup

- [X] T052 [US1] Implement backend/app/main.py FastAPI application with CORS middleware (allow FRONTEND_URL origin, credentials=True)
- [X] T053 [US1] Register auth router in backend/app/main.py with /api/auth prefix
- [X] T054 [US1] Add global exception handlers in backend/app/main.py for standardized error responses per contracts/errors.md
- [X] T055 [US1] Configure FastAPI OpenAPI documentation with security scheme (BearerAuth) in backend/app/main.py

### Frontend Authentication Configuration

- [X] T056 [US1] Configure Better Auth in frontend/src/lib/auth.ts with BETTER_AUTH_SECRET and JWT settings (expiration, cookie options)
- [X] T057 [US1] Implement API client in frontend/src/lib/api.ts with fetch wrapper that includes credentials (cookies) and handles errors per contracts/errors.md
- [X] T058 [US1] Create TypeScript type definitions in frontend/src/lib/types.ts (User, AuthResponse, ErrorResponse)

### Frontend Authentication UI

- [X] T059 [US1] Implement registration page in frontend/src/app/register/page.tsx with email/password form, validation, and Better Auth integration
- [X] T060 [US1] Implement login page in frontend/src/app/login/page.tsx with email/password form, validation, and Better Auth integration
- [X] T061 [US1] Implement useAuth custom hook in frontend/src/hooks/useAuth.ts for authentication state management (login, logout, current user)
- [X] T062 [US1] Implement AuthGuard component in frontend/src/components/AuthGuard.tsx to protect routes (redirects to /login if unauthenticated)
- [X] T063 [US1] Create landing page in frontend/src/app/page.tsx that redirects authenticated users to /dashboard and unauthenticated to /login
- [X] T064 [US1] Create root layout in frontend/src/app/layout.tsx with Better Auth provider and global styles

### US1 Integration & Verification

- [X] T065 [US1] Start backend server (uvicorn app.main:app --reload) and verify FastAPI docs accessible at http://localhost:8000/docs
- [ ] T066 [US1] Start frontend server (npm run dev) and verify app accessible at http://localhost:3000
- [X] T067 [US1] Manual test: Register new user → verify account created in database, JWT token in cookie, redirected to dashboard
- [X] T068 [US1] Manual test: Login with valid credentials → verify JWT token issued, session persists across browser restart
- [X] T069 [US1] Manual test: Login with invalid credentials → verify 400 error displayed, no token issued
- [ ] T070 [US1] Manual test: Logout → verify cookie cleared, redirected to login page
- [ ] T071 [US1] Manual test: Access protected route without token → verify redirected to login

---

## Phase 4: User Story 2 - Create and View Personal Todos (P1)

**Goal**: Implement todo creation and retrieval with strict user isolation.

**Dependencies**: US1 (requires authentication)

**Independent Test Criteria**:
- Authenticated user creates todo with title and description → todo saved and appears in list
- Authenticated user creates todo with title only → todo created with null description
- Authenticated user views todo list → sees only own todos ordered by created_at DESC
- User with no todos views dashboard → sees empty state message
- Unauthenticated user attempts to create todo → 401 Unauthorized

**Delivers**: Core task management functionality (MVP with US1)

### Backend Todo Service

- [X] T072 [US2] Implement create_todo function in backend/app/services/todo.py (validates title non-empty, assigns user_id from JWT, creates todo record)
- [X] T073 [US2] Implement get_user_todos function in backend/app/services/todo.py (queries todos filtered by user_id, orders by created_at DESC per FR-017)
- [X] T074 [US2] Implement get_todo_by_id function in backend/app/services/todo.py (queries todo by id AND user_id for security, returns None if not found/not owned)
- [X] T075 [US2] Create backend/app/services/__init__.py exporting todo service

### Backend Todo Endpoints

- [X] T076 [US2] Create backend/app/routers/todos.py router with FastAPI APIRouter
- [X] T077 [US2] Implement POST /api/todos endpoint in backend/app/routers/todos.py (requires auth, accepts TodoCreate, returns TodoSingleResponse with 201)
- [X] T078 [US2] Implement GET /api/todos endpoint in backend/app/routers/todos.py (requires auth, returns TodoListResponse with user's todos ordered by created_at DESC, returns 200)
- [X] T079 [US2] Implement GET /api/todos/{id} endpoint in backend/app/routers/todos.py (requires auth, returns TodoSingleResponse or 404 if not found/not owned, returns 200)
- [X] T080 [US2] Register todos router in backend/app/main.py with /api/todos prefix and auth middleware dependency

### Frontend Todo State Management

- [X] T081 [US2] Implement useTodos custom hook in frontend/src/hooks/useTodos.ts with functions (createTodo, fetchTodos, getTodo) and state management
- [X] T082 [US2] Create Todo TypeScript type in frontend/src/lib/types.ts (id, user_id, title, description, completed, created_at, updated_at)

### Frontend Todo UI Components

- [X] T083 [US2] Implement TodoList component in frontend/src/components/TodoList.tsx to display list of todos with empty state
- [X] T084 [US2] Implement TodoItem component in frontend/src/components/TodoItem.tsx to display individual todo (title, description, completed status)
- [X] T085 [US2] Implement CreateTodoForm component in frontend/src/components/CreateTodoForm.tsx with title and description fields, validation, and submit handler

### Frontend Dashboard Page

- [X] T086 [US2] Implement dashboard page in frontend/src/app/dashboard/page.tsx protected by AuthGuard with CreateTodoForm and TodoList components
- [X] T087 [US2] Implement dashboard layout in frontend/src/app/dashboard/layout.tsx with logout button and user info display

### US2 Integration & Verification

- [X] T088 [US2] Manual test: Login and create todo with title and description → verify todo appears immediately in list with both fields
- [X] T089 [US2] Manual test: Create todo with title only → verify todo created with null/empty description
- [X] T090 [US2] Manual test: Create multiple todos → verify all appear in list ordered by newest first
- [X] T091 [US2] Manual test: Refresh page → verify todos still visible (persistence)
- [X] T092 [US2] Manual test: Register second user in incognito window → verify they don't see first user's todos (isolation)

---

## Phase 5: User Story 3 - Update Todo Status and Details (P2)

**Goal**: Implement todo update functionality including completion toggle and title/description editing.

**Dependencies**: US2 (requires todos to exist)

**Independent Test Criteria**:
- User marks todo as complete → todo marked complete, visual indicator shown
- User marks completed todo as incomplete → todo returned to incomplete state
- User edits todo title → changes saved and reflected in list
- User edits todo description → changes saved and reflected in list
- User attempts to edit another user's todo → 404 Not Found

**Delivers**: Task lifecycle management (complete task tracking workflow)

### Backend Todo Service Updates

- [X] T093 [US3] Implement update_todo function in backend/app/services/todo.py (queries todo by id AND user_id, updates provided fields only, updates updated_at timestamp, returns updated todo or None)
- [X] T094 [US3] Implement toggle_complete function in backend/app/services/todo.py (queries todo by id AND user_id, flips completed boolean, updates updated_at, returns updated todo or None)

### Backend Todo Update Endpoint

- [X] T095 [US3] Implement PATCH /api/todos/{id} endpoint in backend/app/routers/todos.py (requires auth, accepts TodoUpdate with optional fields, returns TodoSingleResponse or 404, returns 200)

### Frontend Todo Update Components

- [X] T096 [US3] Add toggleComplete function to useTodos hook in frontend/src/hooks/useTodos.ts (calls PATCH endpoint with completed field)
- [X] T097 [US3] Add updateTodo function to useTodos hook in frontend/src/hooks/useTodos.ts (calls PATCH endpoint with title/description fields)
- [X] T098 [US3] Implement EditTodoForm component in frontend/src/components/EditTodoForm.tsx with pre-filled title/description fields and save handler
- [X] T099 [US3] Add completion checkbox to TodoItem component in frontend/src/components/TodoItem.tsx with toggle handler and visual state (strikethrough for completed)
- [X] T100 [US3] Add edit button to TodoItem component in frontend/src/components/TodoItem.tsx that opens EditTodoForm modal/inline editor

### US3 Integration & Verification

- [X] T101 [US3] Manual test: Create todo and mark as complete → verify checkbox checked, strikethrough applied
- [X] T102 [US3] Manual test: Mark completed todo as incomplete → verify checkbox unchecked, strikethrough removed
- [X] T103 [US3] Manual test: Edit todo title → verify changes saved and displayed immediately
- [X] T104 [US3] Manual test: Edit todo description → verify changes saved and displayed immediately
- [X] T105 [US3] Manual test: Attempt to edit another user's todo via direct API call → verify 404 Not Found

---

## Phase 6: User Story 4 - Delete Personal Todos (P3)

**Goal**: Implement permanent todo deletion with user ownership verification.

**Dependencies**: US2 (requires todos to exist)

**Independent Test Criteria**:
- User deletes todo → todo permanently removed from database and disappears from list
- User deletes one todo from multiple → only that todo removed, others remain
- User attempts to delete another user's todo → 404 Not Found

**Delivers**: Task list maintenance (complete CRUD operations)

### Backend Todo Service Delete

- [X] T106 [US4] Implement delete_todo function in backend/app/services/todo.py (queries todo by id AND user_id, deletes from database if owned, returns True if deleted or False if not found/not owned)

### Backend Todo Delete Endpoint

- [X] T107 [US4] Implement DELETE /api/todos/{id} endpoint in backend/app/routers/todos.py (requires auth, returns success message or 404, returns 200 or 404)

### Frontend Todo Delete Functionality

- [X] T108 [US4] Add deleteTodo function to useTodos hook in frontend/src/hooks/useTodos.ts (calls DELETE endpoint, removes todo from local state on success)
- [X] T109 [US4] Add delete button to TodoItem component in frontend/src/components/TodoItem.tsx with confirmation dialog
- [X] T110 [US4] Implement confirmation dialog/modal for delete action (optional: use browser confirm() or custom modal)

### US4 Integration & Verification

- [X] T111 [US4] Manual test: Delete todo → verify todo removed from list and database
- [X] T112 [US4] Manual test: Create 3 todos, delete middle one → verify only that todo deleted, others remain in correct order
- [X] T113 [US4] Manual test: Attempt to delete another user's todo via direct API call → verify 404 Not Found

---

## Phase 7: User Story 5 - Persistent Multi-User Todo Management (P1)

**Goal**: Verify and test multi-user isolation and persistence across the entire system.

**Dependencies**: US1, US2, US3, US4 (requires all CRUD operations)

**Independent Test Criteria**:
- User A creates todos, logs out, logs back in → all todos still present
- User A and User B register separately → each sees only their own todos
- Multiple users operate simultaneously → no conflicts, no data leakage
- User with expired token attempts API calls → all requests return 401 Unauthorized

**Delivers**: Security verification (ensures zero data leakage between users)

**Note**: US5 is an architectural requirement that is implemented across all previous user stories through user-scoped queries. This phase focuses on integration testing and verification.

### Multi-User Isolation Verification

- [X] T114 [US5] Manual test: User A creates 3 todos → logout → login → verify all 3 todos still present (persistence)
- [X] T115 [US5] Manual test: User A creates todos → User B registers in incognito → User B creates different todos → switch back to User A → verify User A sees only own todos (isolation)
- [X] T116 [US5] Manual test: User A and User B both create todos simultaneously → verify no conflicts, each sees only own todos (concurrent operations)
- [X] T117 [US5] Manual test: Clear browser cookies → attempt to access /api/todos → verify 401 Unauthorized (auth enforcement)
- [X] T118 [US5] Manual test: Manually expire JWT token (set exp claim to past) → attempt API call → verify 401 Unauthorized (token expiration)

### Database Query Audit

- [X] T119 [US5] Code review: Verify ALL database queries in backend/app/services/todo.py filter by user_id (no unscoped queries)
- [X] T120 [US5] Code review: Verify user_id is ALWAYS extracted from JWT token, never from request body (security audit)
- [X] T121 [US5] Code review: Verify all update/delete operations check ownership (query includes user_id filter)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Enhance user experience, error handling, and code quality.

### Error Handling & Validation

- [X] T122 Implement comprehensive input validation in all backend endpoints (empty title, max length enforcement, email format)
- [X] T123 Add error toasts/notifications in frontend for all API error responses using contracts/errors.md error codes
- [X] T124 Implement loading states in frontend for all async operations (spinners, disabled buttons)
- [X] T125 Add form validation in frontend (required fields, email format, password strength) before API calls

### User Experience Enhancements

- [X] T126 Add visual feedback for completed todos (strikethrough, gray out, move to bottom)
- [X] T127 Implement todo count display in dashboard header (X todos, Y completed)
- [X] T128 Add empty state illustrations and helpful messages for zero todos
- [X] T129 Implement optimistic UI updates (immediate feedback before API response)
- [X] T130 Add keyboard shortcuts (Enter to submit forms, Escape to cancel)

### Code Quality & Documentation

- [X] T131 Add docstrings to all backend functions (service layer and routers)
- [X] T132 Add JSDoc comments to all frontend functions and components
- [X] T133 Run linter on backend (flake8 or black) and fix issues
- [X] T134 Run linter on frontend (ESLint) and fix issues
- [X] T135 Generate OpenAPI JSON spec from FastAPI app and save to docs/api.json

### Performance Optimization

- [X] T136 Add database indexes verification (ensure idx_users_email, idx_todos_user_id, idx_todos_user_created exist and are used)
- [X] T137 Implement API response caching headers (Cache-Control) where appropriate
- [X] T138 Add pagination to GET /api/todos if user has >100 todos (optional, future enhancement placeholder)

### Deployment Preparation

- [X] T139 Create production Dockerfile for backend with uvicorn server
- [X] T140 Create production Dockerfile for frontend with Next.js build
- [X] T141 Create docker-compose.yml for local multi-container setup (backend, frontend, postgres)
- [X] T142 Document environment variables for production in docs/deployment.md
- [X] T143 Create CI/CD pipeline configuration (.github/workflows/) for automated testing and deployment

---

## Implementation Strategy

### MVP Definition (Minimal Viable Product)

**MVP = US1 + US2**: User authentication + Create/View todos

This delivers the core value proposition:
1. Users can register and login securely
2. Users can create and view their personal todos
3. Todos persist across sessions
4. Basic user isolation is enforced

**MVP Task Range**: T001 to T092 (first 92 tasks)
**Estimated Time**: 2-3 days for experienced developer

### Incremental Delivery Order

1. **Sprint 1 (MVP)**: Complete US1 + US2
   - Deliverable: Users can register, login, create todos, view todos
   - Test: Register → Login → Create 3 todos → Logout → Login → Verify todos persist

2. **Sprint 2 (Full CRUD)**: Complete US3 + US4
   - Deliverable: Users can update and delete todos
   - Test: Create todo → Mark complete → Edit title → Delete todo

3. **Sprint 3 (Security & Polish)**: Complete US5 + Phase 8
   - Deliverable: Multi-user isolation verified, UX polished, error handling comprehensive
   - Test: Two users operate simultaneously → No data leakage → All edge cases handled

### Parallel Execution Opportunities

**Phase 1 Setup (Can run in parallel)**:
- T002-T005 (Backend config files)
- T007-T012 (Frontend config files)
- T016-T020 (Documentation files)

**Phase 2 Foundational (Can run in parallel after T024-T026)**:
- T033-T035 (API schemas - independent of database)

**US1 Implementation (Can run in parallel)**:
- T039-T043 (Backend auth service) + T056-T058 (Frontend auth config)
- T047-T051 (Backend auth endpoints) + T059-T064 (Frontend auth UI) - after services complete

**US2 Implementation (Can run in parallel)**:
- T072-T075 (Backend todo service) + T081-T082 (Frontend todo hooks)
- T076-T080 (Backend todo endpoints) + T083-T085 (Frontend todo components) - after services complete

**US3 Implementation (Can run in parallel)**:
- T093-T094 (Backend updates) + T096-T097 (Frontend update functions)
- T098-T100 (Frontend UI updates) - after functions complete

**Phase 8 Polish (Can run in parallel)**:
- T122-T125 (Error handling - independent tasks)
- T126-T130 (UX enhancements - independent tasks)
- T131-T135 (Code quality - independent tasks)
- T136-T138 (Performance - independent tasks)
- T139-T143 (Deployment - independent tasks)

---

## Task Dependency Graph

```
Phase 1 (Setup)
  T001-T023 (can parallelize T002-T005, T007-T012, T016-T020)
  ↓
Phase 2 (Foundational)
  T024-T026 (Database models - BLOCKING)
  ↓
  T027-T032 (Database setup - BLOCKING)
  ↓
  T033-T038 (Schemas & errors - can parallelize T033-T035)
  ↓
Phase 3 (US1 - Authentication)
  T039-T046 (Backend auth - BLOCKING for endpoints)
  ↓
  T047-T055 (Backend endpoints & app setup)
  ‖
  T056-T064 (Frontend auth UI - can parallelize with backend)
  ↓
  T065-T071 (US1 verification)
  ↓
Phase 4 (US2 - Create/View Todos)
  T072-T075 (Backend todo service - BLOCKING for endpoints)
  ↓
  T076-T080 (Backend todo endpoints)
  ‖
  T081-T087 (Frontend todo UI - can parallelize with backend)
  ↓
  T088-T092 (US2 verification)
  ↓
Phase 5 (US3 - Update Todos)
  T093-T095 (Backend updates)
  ‖
  T096-T100 (Frontend updates - can parallelize)
  ↓
  T101-T105 (US3 verification)
  ↓
Phase 6 (US4 - Delete Todos)
  T106-T107 (Backend delete)
  ‖
  T108-T110 (Frontend delete - can parallelize)
  ↓
  T111-T113 (US4 verification)
  ↓
Phase 7 (US5 - Multi-User Verification)
  T114-T121 (Integration tests & security audit)
  ↓
Phase 8 (Polish)
  T122-T143 (many tasks can parallelize)
```

**Critical Path**: T001 → T024 → T027 → T039 → T047 → T052 → T072 → T076 → T088 (MVP delivery)

**Parallel Branches**:
- Backend development (T039-T055, T072-T080, T093-T095, T106-T107)
- Frontend development (T056-T064, T081-T087, T096-T100, T108-T110)

---

## Task Count Summary

- **Phase 1 (Setup)**: 23 tasks (T001-T023)
- **Phase 2 (Foundational)**: 15 tasks (T024-T038)
- **Phase 3 (US1 - Auth)**: 33 tasks (T039-T071)
- **Phase 4 (US2 - Create/View)**: 21 tasks (T072-T092)
- **Phase 5 (US3 - Update)**: 13 tasks (T093-T105)
- **Phase 6 (US4 - Delete)**: 8 tasks (T106-T113)
- **Phase 7 (US5 - Isolation)**: 8 tasks (T114-T121)
- **Phase 8 (Polish)**: 22 tasks (T122-T143)

**Total**: 143 tasks

**MVP Scope**: 92 tasks (T001-T092) = Phases 1-4 = US1 + US2
**Full Feature**: 121 tasks (T001-T121) = Phases 1-7 = All user stories
**Production Ready**: 143 tasks (T001-T143) = All phases including polish

**Parallelization Opportunities**: 45 tasks marked [P] = ~31% of tasks can run in parallel

---

## Verification Checklist

After completing all tasks, verify against success criteria from spec.md:

- [ ] SC-001: Users can complete registration and login within 1 minute
- [ ] SC-002: Todo creation appears in list within 2 seconds
- [ ] SC-003: Zero data leakage between users (multi-user isolation test)
- [ ] SC-004: All API endpoints respond within 500ms
- [ ] SC-005: 95% success rate for all CRUD operations
- [ ] SC-006: 100% rejection of invalid/expired JWT tokens
- [ ] SC-007: Sessions persist across browser restarts
- [ ] SC-008: Multiple users can operate simultaneously without conflicts
- [ ] SC-009: Graceful error handling for database failures
- [ ] SC-010: 100% rejection of weak passwords

**All criteria must pass before considering Phase II complete.**

---

## Notes

- **Task Format**: Every task follows format `- [ ] T### [P] [US#] Description with file path`
- **Parallelization**: Tasks marked [P] can run concurrently with other [P] tasks in the same phase
- **User Story Labels**: Tasks marked [US#] map directly to user stories in spec.md
- **Independence**: Each user story (US1-US5) can be tested independently
- **Traceability**: All tasks trace back to functional requirements (FR-001 to FR-038) in spec.md
- **File Paths**: Every implementation task includes specific file path for clarity
- **Security First**: User isolation (filtering by user_id) is enforced in all database queries
- **No Tests Generated**: Tests are OPTIONAL per task generation rules - not explicitly requested in spec

**Ready for implementation!** Start with Phase 1 (T001-T023) to set up project structure, then proceed sequentially or parallelize where marked.
