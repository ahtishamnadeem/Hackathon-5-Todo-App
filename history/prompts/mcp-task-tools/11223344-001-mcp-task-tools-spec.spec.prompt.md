---
id: 11223344-001-mcp-task-tools-spec
title: MCP Server & Task Tools Specification
stage: spec
date: 2026-01-21
feature: mcp-task-tools
author: Claude
version: 1.0.0
surface: agent
model: claude-sonnet-4-5-20250929
branch: 001-mcp-task-tools
user: user
---

# Prompt

sp.specify

MCP Server & Task Tools --- Objective:
Design and implement a stateless MCP (Model Context Protocol) server that exposes todo task operations as tools usable by an AI agent. The MCP server must act as the execution layer for the AI system, persisting all state in the database while remaining fully stateless between requests.

Target audience:
Hackathon reviewers and technical evaluators assessing MCP compliance, tool design, and agent-safe execution layers.

Core responsibilities:
- Provide MCP-compliant tools for task management
- Enforce user isolation and data integrity
- Persist all state changes to the database
- Expose deterministic, machine-readable tool responses
- Remain stateless and idempotent where possible

Success criteria:
- AI agent can invoke MCP tools to manage tasks reliably
- All task operations are scoped strictly to the requesting user
- Tools do not maintain in-memory state
- Tool inputs and outputs follow clear, validated schemas
- Errors are handled gracefully and consistently
- MCP server integrates cleanly wit --- Tool execution rules:
- Every tool invocation must include user_id
- Tools must never infer user identity implicitly
- All reads and writes must go through the database
- Tools must not call other tools
- Tools must not depend on request ordering or previous calls

MCP tools specification:

Tool: add_task
Purpose:
Create a new todo task

Parameters:
- user_id (string, required)
- title (string, required)
- description (string, optional)

Behavior:
- Create a new task associated with user_id
- Default completed status to false
- Persist timestamps --- Returns:
- task_id (integer)
- status ("created")
- title (string)

---

Tool: list_tasks
Purpose:
Retrieve tasks for a user

Parameters:
- user_id (string, required)
- status (string, optional: "all", "pending", "completed")

Behavior:
- Return tasks belonging only to user_id
- Apply filter if provided
- Sort by creation time (ascending)

Returns:
- Array of task objects (id, title, completed)

---

Tool: complete_task
Purpose:
Mark a task as completed

Parameters:
- user_id (string, required)
- task_id (integer, required) --- Behavior:
- Verify task exists and belongs to user
- Update completed status to true
- Update timestamp

Returns:
- task_id (integer)
- status ("completed")
- title (string)

---

Tool: update_task
Purpose:
Modify task title or description

Parameters:
- user_id (string, required)
- task_id (integer, required)
- title (string, optional)
- description (string, optional)

Behavior:
- Verify task ownership
- Update provided fields only
- Persist changes

Returns:
- task_id (integer)
- status ("updated")
- title (string)

---

Tool: delete_task
Purpose:
Remove a task --- Parameters:
- user_id (string, required)
- task_id (integer, required)

Behavior:
- Verify task ownership
- Delete task permanently

Returns:
- task_id (integer)
- status ("deleted")
- title (string)

Error handling:
- If task does not exist → return structured error
- If task does not belong to user → return authorization error
- If parameters are invalid → return validation error
- Errors must be machine-readable and agent-friendly
- No raw exceptions or stack traces --- Statelessness requirements:
- MCP server must not store session or conversation state
- Each tool invocation must be independently executable
- Server restarts must not affect correctness

Database requirements:
- Use SQLModel ORM
- Use Neon Serverless PostgreSQL
- All task queries must be indexed by user_id
- Transactions must be atomic

Security:
- MCP tools must be callable only by authenticated agent backend
- user_id passed to tools must already be validated by backend
- Tools must never trust external or frontend input directly --- Constraints:
- No AI logic inside MCP tools
- No frontend logic inside MCP server
- No caching or in-memory persistence
- No cross-user operations

Not building:
- Bulk task operations
- Task prioritization
- Scheduling or reminders
- Soft deletes or archives
- Audit logging dashboards

Deliverables:
- MCP server implemented using Official MCP SDK
- Five stateless task management tools
- Database-backed persistence layer
- Tool schemas and contracts
- Clean integration point for AI agent
- Spec-compliant, review-ready codebase

# Response

## MCP Server & Task Tools Specification Created Successfully

I've successfully created the specification for the MCP Server & Task Tools feature. The specification includes:

### Key Features Defined
- Five MCP-compliant tools: add_task, list_tasks, complete_task, update_task, delete_task
- Stateless operation with no session storage
- Strict user isolation and data integrity
- Deterministic, machine-readable responses
- Proper error handling and validation

### User Stories
1. **AI Agent Task Management (P1)** - Core functionality for AI agents to manage tasks
2. **Secure User Isolation (P1)** - Ensuring data security between users
3. **Deterministic Tool Execution (P1)** - Consistent responses for AI consumption
4. **Stateless Operation (P2)** - Scalable and reliable operation

### Requirements
- 12 functional requirements covering tool behavior, validation, security, and error handling
- Clear success criteria with measurable outcomes
- Identified edge cases for robust implementation

The specification is now ready for the next phase. You can proceed with `/sp.plan` to create an implementation plan based on this specification.