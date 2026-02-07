<!--
Sync Impact Report
- Version change: 2.0.0 -> 3.0.0 (MAJOR)
- List of modified principles:
  - Added Principle IX: Agentic Architecture & MCP Standards
  - Added Principle X: Stateless-by-Design Architecture
  - Added Principle XI: Observability & Traceability
- Expanded Phase III definition with complete AI/MCP architecture requirements
- Added sections:
  - Phase III AI System Standards
  - MCP Server Standards
  - Conversation & Memory Standards
  - Security Extensions for AI/MCP
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md (Logic checked)
  - ✅ .specify/templates/spec-template.md (Logic checked)
  - ✅ .specify/templates/tasks-template.md (Logic checked)
- Follow-up TODOs: Create Phase III spec, plan, and tasks documents
- Rationale: Phase III introduces AI-powered chatbot with agentic architecture requiring mandatory MCP standards, stateless design, and observability that fundamentally change project architecture requirements
-->
## Multi-Phase Todo Application Constitution

## Vision
Build a progressive Todo application that evolves from a simple in-memory Python console app into a production-grade, AI-powered, cloud-native system.

## Core Principles

### I. Simplicity First, Scalability Later
Start with the simplest viable implementation. Do not introduce abstractions for future phases until those phases are actively being implemented. Clear, readable code is prioritized over premature optimization.

### II. Clear Separation of Concerns
Maintain strict boundaries between domain logic, interface layers, and storage mechanisms. This ensures that the core logic can remain stable even as the frontend or database technology changes across phases.

### III. Spec-Driven Development (SDD)
Every phase must be built against verified specifications. No implementation should begin without a clear plan, defined tasks, and acceptance criteria. All changes must be small, testable, and documented in PHRs.

### IV. Determinism Before Augmentation
Core business logic must behave deterministically. AI features introduced in later phases act as an interface layer or an enhancement, never as the primary owner of the application's business rules.

### V. Developer-Friendly and Testable
The codebase must favor clarity over cleverness. Every component should be easy to run locally, test independently, and understand without deep domain knowledge. Explicit assumptions are always preferred over implicit behavior.

### VI. Security-First Architecture
From Phase II onward, security is non-negotiable. All multi-user systems must enforce strict user isolation, secure authentication, and data scoping. No user should ever access another user's data. Security must be baked into the architecture, not bolted on afterward.

### VII. Correctness by Design
All features must be implemented exactly as specified. Every implementation must be traceable to an explicit spec. Deviations from spec are treated as bugs. Tests must verify that the system behaves exactly as documented.

### VIII. Production Readiness
From Phase II onward, code must be production-ready. This includes proper error handling, validation, logging, and adherence to REST API standards. Stateless backend architecture ensures horizontal scalability. All endpoints must follow HTTP status code conventions and provide meaningful error messages.

### IX. Agentic Architecture & MCP Standards
From Phase III onward, AI-powered features must operate through well-defined Machine Control Protocol (MCP) tools. AI agents must never bypass business logic and must strictly delegate execution to MCP tools. Natural language understanding is handled by the AI agent; execution is handled by MCP tools with explicit schemas and validation.

### X. Stateless-by-Design Architecture
All backend services and MCP tools must remain stateless. No in-memory session state is allowed. All state must persist in the database. Server must rebuild context on every request. This ensures horizontal scalability and fault tolerance across all phases.

### XI. Observability & Traceability
All agent actions (messages, tool calls, results) must be persisted and auditable. Conversation state must be persisted in the database. Server must maintain complete traceability of all AI interactions. This enables debugging, monitoring, and compliance across all system phases.

## Phase Definitions

### Phase I – In-Memory Python Console App
- **Technology**: Python
- **Storage**: In-memory (no persistence)
- **Interface**: Console / CLI
- **Non-negotiable**: Must remain dependency-free. Establish correct domain logic boundaries.

### Phase II – Full-Stack Web Application
- **Frontend**: Next.js 16+ (App Router, React Server Components, Server Actions)
- **Backend**: Python FastAPI (stateless REST API)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL (managed cloud database)
- **Authentication**: Better Auth (JWT-based token authentication)
- **Focus**: Transition from memory to persistence. Implement secure RESTful API with JWT authentication, strict user isolation, and client-server separation. All features must be production-ready with proper error handling and validation.

### Phase III – AI-Powered Todo Chatbot with Agentic Architecture
- **AI Agent**: OpenAI Agents SDK with MCP tools
- **MCP Server**: Official MCP SDK with stateless tools
- **Architecture**: Agentic design with explicit reasoning delegation
- **Focus**: Natural language interaction with deterministic tool execution. AI handles natural language understanding while MCP tools handle execution. All agent actions must be persistent and auditable. System must remain secure, stateless, and scalable.

### Phase IV – Local Kubernetes Deployment
- **Stack**: Docker, Minikube, Helm, kubectl-ai
- **Focus**: Service orchestration and local cloud simulation.

### Phase V – Advanced Cloud Deployment
- **Stack**: DigitalOcean DOKS, Kafka, Dapr
- **Focus**: Event-driven architecture, scalability, and production patterns.

## Development Standards & Constraints

### Constraints
- **Phase Isolation**: Earlier phases must NOT depend on later-phase technologies.
- **AI restriction**: No AI features or logic before Phase III.
- **Cloud restriction**: No Kubernetes or cloud abstractions before Phase IV.
- **Upgrade Path**: Each phase must include a documented strategy for migrating or upgrading to the next phase.

### Non-Goals
- Premature optimization.
- Over-engineering early phases.
- Mixing AI logic into core domain logic.

## Phase II Security Requirements

### Authentication & Authorization
- **JWT Tokens**: All API requests (except registration/login) must include a valid JWT token in the Authorization header.
- **Token Storage**: Frontend stores JWT in httpOnly cookies (secure, not accessible via JavaScript).
- **User Isolation**: All database queries must be scoped to the authenticated user. No user can access another user's todos.
- **Better Auth Integration**: Use Better Auth library for user management, token generation, and validation.

### Data Scoping
- **User-Scoped Queries**: Every todo query must include `WHERE user_id = <authenticated_user_id>`.
- **Creation Enforcement**: When creating a todo, the `user_id` is automatically set from the JWT token, not from request body.
- **Update/Delete Guards**: Users can only modify/delete their own todos. Attempting to modify another user's todo returns 404 (not 403, to prevent data leakage).

### API Security Standards
- **CORS Configuration**: Restrict CORS to frontend domain only (not wildcard).
- **Rate Limiting**: Implement rate limiting to prevent abuse.
- **Input Validation**: All inputs must be validated using Pydantic models. Reject invalid data with 400 Bad Request.
- **SQL Injection Prevention**: Use SQLModel parameterized queries (never string concatenation).
- **Password Security**: Passwords must be hashed using bcrypt or argon2 (never stored in plaintext).

## Phase III AI & MCP Security Requirements

### AI Agent Security
- **JWT Authentication**: All chat endpoints require valid JWT authentication.
- **User Identity**: User identity must be derived exclusively from verified JWT.
- **Agent Context**: AI agents and MCP tools must be scoped to authenticated user context.
- **Cross-User Isolation**: Cross-user data access must be impossible at all layers.

### MCP Tool Security
- **User-Scoped Operations**: All MCP tools must enforce user isolation through JWT-derived user_id.
- **Tool Validation**: MCP tools must validate all inputs and reject unauthorized operations.
- **Stateless Operation**: MCP tools must not maintain any session state, relying solely on JWT and database.

### Conversation Security
- **User-Specific Persistence**: Conversation history must be user-scoped and secure.
- **Authentication Required**: All chat endpoints require valid JWT authentication.
- **Identity Verification**: All AI operations must verify user identity from JWT before execution.

## REST API Conventions

### HTTP Methods
- `GET`: Retrieve resources (idempotent, safe)
- `POST`: Create new resources
- `PUT`: Replace entire resource (idempotent)
- `PATCH`: Partial update of resource
- `DELETE`: Remove resource (idempotent)

### HTTP Status Codes
- `200 OK`: Successful GET, PUT, PATCH, or DELETE
- `201 Created`: Successful POST (resource created)
- `204 No Content`: Successful DELETE with no response body
- `400 Bad Request`: Invalid input, validation errors
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Valid token but insufficient permissions (avoid when possible; prefer 404 for security)
- `404 Not Found`: Resource does not exist or user doesn't have access
- `500 Internal Server Error`: Unexpected server error

### Response Format
All API responses must follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or for errors:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title is required",
    "details": { "field": "title" }
  }
}
```

## MCP Tool Conventions

### Tool Structure
- **Stateless**: MCP tools must not maintain session state
- **Validated**: All inputs must be validated before execution
- **User-Scoped**: All operations must respect JWT-derived user identity
- **Structured**: Tools must return consistent, structured responses

### Tool Response Format
All MCP tool responses must follow this structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Or for errors:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "TOOL_ERROR",
    "message": "Operation failed",
    "details": { "reason": "specific reason" }
  }
}
```

## Data Persistence Constraints

### Database Schema
- **User Table**: `id`, `email`, `password_hash`, `created_at`, `updated_at`
- **Todo Table**: `id`, `user_id` (FK), `title`, `description`, `completed`, `created_at`, `updated_at`
- **Conversation Table**: `id`, `user_id` (FK), `title`, `created_at`, `updated_at` (Phase III)
- **Message Table**: `id`, `conversation_id` (FK), `role`, `content`, `timestamp` (Phase III)
- **Indexes**: Create indexes on `user_id` for performance
- **Constraints**: `user_id` is NOT NULL, foreign key with CASCADE delete

### Migration Strategy
- Use Alembic for database migrations
- All schema changes must have both upgrade and downgrade paths
- Migrations must be tested before deployment

### Backup & Recovery
- Neon PostgreSQL provides automatic backups
- Document recovery procedures in operations runbook

## Governance

### Amendment Procedure
This constitution is the authoritative source for project rules. Significant changes require:
1. An update to this document.
2. A corresponding version bump.
3. Creation of an ADR to document the rationale if the change is architecturally significant.

### Versioning Policy
- **MAJOR**: Backward incompatible governance/principle changes.
- **MINOR**: New sections or expanded guidance.
- **PATCH**: Typos or wording clarifications.

**Version**: 3.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-11