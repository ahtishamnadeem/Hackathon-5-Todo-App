# Research: Phase I – In-Memory Python Console Todo App

## Decision: Layered Architecture
**Rationale**: Even for a simple app, a layered approach (Domain -> Repository -> Service -> CLI) ensures that Phase II (persistence) can be implemented by just swapped the Repository layer, without touching business logic or UI.
**Alternatives considered**: Single module script (rejected as it violates Phase I goal of established domain boundaries).

## Decision: Python Native Types for Storage
**Rationale**: Using a Python `list` of `Todo` objects or a `dict` (ID -> Todo) provides the fastest, most direct implementation for in-memory storage without external dependencies. A `dict` is preferred for O(1) lookups by ID.
**Alternatives considered**: `InMemorySqlite` (rejected to keep it truly dependency-free and "simple first").

## Decision: Command-Line Menu System
**Rationale**: A simple numeric input menu (1-5) is deterministic and easy to validate.
**Alternatives considered**: Command-line arguments (`todo add "title"`) (rejected for Phase I to favor interactive session as per spec).
