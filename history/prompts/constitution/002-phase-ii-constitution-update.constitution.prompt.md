---
id: 2
title: Phase II Constitution Update
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: default
command: /sp.constitution
labels: [constitution, phase-ii, security, jwt, authentication]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - CLAUDE.md
tests:
  - none
---

## Prompt

Project: Todo Full-Stack Web Application (Spec-Driven Development – Hackathon Phase-2)

Core principles:
- Correctness by design (all features implemented exactly as specified)
- Security-first architecture (JWT-based authentication and strict user isolation)
- Spec-driven development (every implementation traceable to an explicit spec)
- Production readiness (stateless backend, proper error handling, REST standards)

Phase II Requirements:

Frontend:
- Next.js 16+ (App Router)
- React Server Components
- Server Actions
- Better Auth for JWT authentication

Backend:
- Python FastAPI (stateless REST API)
- SQLModel (Pydantic + SQLAlchemy) for ORM
- Neon Serverless PostgreSQL (managed cloud database)
- JWT token-based authentication

Security Requirements:
- All API endpoints (except registration/login) require valid JWT token
- User isolation: every user can only access their own todos
- Data scoping: all queries must include `WHERE user_id = <authenticated_user_id>`
- httpOnly cookies for token storage (not accessible via JavaScript)
- Password hashing: bcrypt or argon2 (never plaintext)
- SQL injection prevention: SQLModel parameterized queries only
- Rate limiting and CORS restrictions

API Standards:
- RESTful conventions (GET/POST/PUT/PATCH/DELETE)
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Standardized response format with success/error structure
- Meaningful error messages with error codes

Data Persistence:
- User table: id, email, password_hash, timestamps
- Todo table: id, user_id (FK), title, description, completed, timestamps
- Indexes on user_id for performance
- Foreign key with CASCADE delete
- Alembic for database migrations

Success Criteria:
- All features implemented exactly as specified
- Security enforced at architecture level (not bolted on)
- Production-ready code with proper validation and error handling
- Clear upgrade path from Phase I in-memory implementation

## Response snapshot

I have successfully updated the project constitution to version 2.0.0 with Phase II requirements. This is a MAJOR version bump because it introduces mandatory new principles that fundamentally change the project's architectural requirements.

Key changes:
1. Added three new core principles:
   - Principle VI: Security-First Architecture
   - Principle VII: Correctness by Design
   - Principle VIII: Production Readiness

2. Expanded Phase II definition with complete tech stack:
   - Frontend: Next.js 16+ with App Router, React Server Components, Server Actions
   - Backend: Python FastAPI (stateless REST API)
   - ORM: SQLModel (Pydantic + SQLAlchemy)
   - Database: Neon Serverless PostgreSQL
   - Authentication: Better Auth (JWT-based)

3. Added comprehensive security requirements section:
   - JWT token authentication for all endpoints (except auth)
   - Strict user isolation with user-scoped queries
   - httpOnly cookies for secure token storage
   - Password hashing standards (bcrypt/argon2)
   - SQL injection prevention via parameterized queries
   - Rate limiting and CORS configuration

4. Added REST API conventions section:
   - HTTP method semantics (GET, POST, PUT, PATCH, DELETE)
   - HTTP status code standards (200, 201, 204, 400, 401, 404, 500)
   - Standardized JSON response format for success/error cases

5. Added data persistence constraints section:
   - Database schema definitions (User and Todo tables)
   - Indexing strategy for performance
   - Foreign key constraints with CASCADE delete
   - Alembic migration strategy with upgrade/downgrade paths
   - Backup and recovery procedures

6. Updated CLAUDE.md development guidelines:
   - Documented constitution version 2.0.0
   - Added Phase II active technologies
   - Outlined Phase II project structure (frontend/backend separation)
   - Added Phase II commands and security standards
   - Updated recent changes with constitution 2.0.0 note

## Outcome

- ✅ Impact: Constitution updated to 2.0.0 with mandatory security, correctness, and production readiness principles for Phase II multi-user web application.
- 🧪 Tests: n/a (constitution document)
- 📁 Files: .specify/memory/constitution.md (v2.0.0), CLAUDE.md (updated)
- 🔁 Next prompts: /sp.specify for Phase II feature specification
- 🧠 Reflection: The MAJOR version bump reflects the fundamental architectural shift from single-user console app to multi-user web application with security-first design. All future Phase II work must strictly adhere to user isolation and JWT authentication requirements.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Begin Phase II specification with /sp.specify
