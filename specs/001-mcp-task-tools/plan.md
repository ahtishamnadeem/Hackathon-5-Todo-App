# Implementation Plan: MCP Server & Task Tools

**Branch**: `001-mcp-task-tools` | **Date**: 2026-01-21 | **Spec**: specs/001-mcp-task-tools/spec.md
**Input**: Feature specification from `/specs/001-mcp-task-tools/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless MCP (Model Context Protocol) server that exposes secure, deterministic task management tools for use by the AI agent. The MCP server acts as the execution layer, persisting all task state to the database while remaining fully stateless between requests. The implementation includes five core tools (add_task, list_tasks, complete_task, update_task, delete_task) that follow MCP standards and ensure user isolation.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Official MCP SDK, FastAPI, SQLModel, PostgreSQL
**Storage**: PostgreSQL database via SQLModel ORM
**Testing**: pytest with contract and integration tests
**Target Platform**: Linux server (cloud deployment ready)
**Project Type**: web (API service with database persistence)
**Performance Goals**: <2s response time for tool execution, 99% success rate
**Constraints**: Stateless execution (no in-memory session storage), strict user isolation, MCP-compliant interfaces
**Scale/Scope**: Multi-user support with secure task operations, integration with existing AI agent

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

**Principle IX. Agentic Architecture & MCP Standards** ✅
- MCP tools operate through well-defined interfaces for the AI agent
- Clear separation between AI reasoning (handled by agent) and execution (handled by MCP tools)
- Explicit schemas and validation for all tool interactions
- AI agents delegate execution to MCP tools as required

**Principle X. Stateless-by-Design Architecture** ✅
- No in-memory session state allowed in MCP tools
- All state persists in database through tool operations
- Each tool invocation is independently executable
- Server restarts do not affect tool correctness

**Principle XI. Observability & Traceability** ✅
- Tool executions can be logged for audit purposes
- All agent actions (tool calls, results) can be persisted
- Complete traceability of AI interactions through tool logs

**Phase III Requirements** ✅
- Uses Official MCP SDK as specified
- MCP server with stateless tools
- Agentic design with explicit reasoning delegation
- Natural language interaction with deterministic tool execution

**Security Requirements** ✅
- MCP tools enforce user isolation via user_id scoping
- All operations validated against authenticated user context
- Tools return 404 for unauthorized access (not 403) to prevent data enumeration
- All operations scoped to authenticated user context

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-task-tools/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── todo.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todo.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todo.py
│   │   └── conversation.py
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py                 # New: MCP server implementation
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── task_tools.py         # New: MCP task management tools
│   │       └── validators.py         # New: Input validation helpers
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todos.py
│   │   └── chat.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── todo_agent.py
│   │   └── agent_runner.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt
```

**Structure Decision**: The implementation extends the existing Phase II backend structure with new modules for MCP server functionality. The MCP server and tools will be added in the new `app/mcp_server/` directory, maintaining separation from the existing FastAPI application structure. The tools will be organized in a dedicated subdirectory for maintainability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | All requirements comply with constitution | N/A |
