# Implementation Plan: AI Agent & Conversation System

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-01-21 | **Spec**: specs/001-ai-todo-chatbot/spec.md
**Input**: Feature specification from `/specs/001-ai-todo-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of the core AI reasoning and conversational layer of Phase-III, enabling users to manage todos through natural language. This plan focuses exclusively on the AI agent, conversation lifecycle, and stateless chat orchestration, excluding MCP tool implementation details and frontend UI concerns. The system will use OpenAI Agents SDK for AI reasoning, with persistent conversation memory via database, and strict separation between agent reasoning and action execution.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: OpenAI Agents SDK, FastAPI, SQLModel, PostgreSQL, MCP SDK
**Storage**: PostgreSQL database via SQLModel ORM
**Testing**: pytest with contract and integration tests
**Target Platform**: Linux server (cloud deployment ready)
**Project Type**: web (API service with database persistence)
**Performance Goals**: <5s response time for chat requests, 95% uptime
**Constraints**: Stateless execution (no in-memory session storage), strict user isolation, JWT authentication required
**Scale/Scope**: Multi-user support with conversation persistence, integration with existing Phase-II components

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

**Principle IX. Agentic Architecture & MCP Standards** ✅
- AI agent will operate through well-defined MCP tools
- Natural language understanding handled by AI agent; execution by MCP tools
- Explicit schemas and validation for all tool interactions

**Principle X. Stateless-by-Design Architecture** ✅
- No in-memory session state allowed
- All state persists in database
- Server rebuilds context on every request
- Conversation history loaded from database per request

**Principle XI. Observability & Traceability** ✅
- All agent actions (messages, tool calls, results) will be persisted
- Conversation state persisted in database
- Complete traceability of all AI interactions

**Phase III Requirements** ✅
- Uses OpenAI Agents SDK as specified
- MCP server with stateless tools
- Agentic design with explicit reasoning delegation
- Natural language interaction with deterministic tool execution

**Security Requirements** ✅
- JWT authentication required for all chat endpoints
- User identity derived exclusively from verified JWT
- User isolation enforced through JWT-derived user_id
- All operations scoped to authenticated user context

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
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
│   │   ├── conversation.py          # New: Conversation entity
│   │   └── message.py               # New: Message entity
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todo.py
│   │   ├── conversation.py          # New: Conversation schema
│   │   └── message.py               # New: Message schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todo.py
│   │   └── conversation.py          # New: Conversation service
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── todos.py
│   │   └── chat.py                  # New: Chat router with AI agent
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── todo_agent.py            # New: AI agent implementation
│   │   └── agent_runner.py          # New: Agent execution orchestrator
│   ├── mcp_tools/
│   │   ├── __init__.py
│   │   └── todo_mcp_tools.py        # New: MCP tools for todo operations
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

**Structure Decision**: The implementation extends the existing Phase II backend structure with new modules for AI agent functionality and conversation persistence. The chat endpoint will be added to the existing FastAPI application, with new models and services for conversation and message entities. The agent implementation will be separate from MCP tools to maintain clear separation of concerns as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
