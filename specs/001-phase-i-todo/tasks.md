---
description: "Task list for Phase I – In-Memory Python Console Todo App implementation"
---

# Tasks: Phase I – In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-phase-i-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Minimal unit tests using pytest will be included for logic verification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo_app/` at repository root
- Paths: `todo_app/domain/`, `todo_app/repository/`, `todo_app/services/`, `todo_app/ui/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure for `todo_app/` per implementation plan
- [x] T002 [P] Initialize Python project with `uv` environment
- [x] T003 [P] Create `__init__.py` files in all `todo_app/` subdirectories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define `Todo` domain entity in `todo_app/domain/todo.py`
- [x] T005 Implement `InMemoryTodoRepository` in `todo_app/repository/memory.py`
- [x] T006 Implement base `TodoService` orchestrator in `todo_app/services/todo_service.py`
- [x] T007 [P] Create `todo_app/main.py` entry point with basic app loop structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Allow users to create tasks and list them in the console.

**Independent Test**: Use CLI to add 2 tasks and then view them. Output must match formatting contract.

### Implementation for User Story 1

- [x] T008 [P] [US1] Implement `create_todo` logic in `todo_app/repository/memory.py`
- [x] T009 [P] [US1] Implement `get_all` logic in `todo_app/repository/memory.py`
- [x] T010 [US1] Map create and list methods in `todo_app/services/todo_service.py`
- [x] T011 [US1] Implement "Add" and "View" menu options in `todo_app/ui/console.py`
- [x] T012 [US1] Implement list formatting logic in `todo_app/ui/console.py`
- [x] T013 [US1] Wire "Add" and "View" actions in `todo_app/main.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Complete and Delete (Priority: P2)

**Goal**: Allow users to toggle task status and remove tasks.

**Independent Test**: Add a task, "Complete" it via CLI, verify status change, then "Delete" it and verify removal.

### Implementation for User Story 2

- [x] T014 [P] [US2] Implement `update` logic for status in `todo_app/repository/memory.py`
- [x] T015 [P] [US2] Implement `delete` logic in `todo_app/repository/memory.py`
- [x] T016 [US2] Add `complete_todo` and `delete_todo` to `todo_app/services/todo_service.py`
- [x] T017 [US2] Implement "Complete" and "Delete" menu options in `todo_app/ui/console.py`
- [x] T018 [US2] Wire "Complete" and "Delete" actions in `todo_app/main.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Update Title (Priority: P3)

**Goal**: Allow users to change the title of an existing task.

**Independent Test**: Add a task, select "Update", change the title, and verify the new title in "View".

### Implementation for User Story 3

- [x] T019 [US3] Implement `update_title` in `todo_app/repository/memory.py`
- [x] T020 [US3] Add `update_todo` to `todo_app/services/todo_service.py`
- [x] T021 [US3] Implement "Update" prompt and menu option in `todo_app/ui/console.py`
- [x] T022 [US3] Wire "Update" action in `todo_app/main.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements

- [x] T023 [P] Add defensive input validation for numeric indices in `todo_app/ui/console.py`
- [x] T024 [P] Final code cleanup and type hint verification across all modules
- [x] T025 Run `quickstart.md` validation to ensure local setup guide is correct

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Phase 1 - BLOCKS all stories.
- **User Stories (Phase 3+)**: All depend on Phase 2 completion.

### Implementation Strategy

- **MVP First**: Complete Phase 1 -> 2 -> 3. Validate US1 before proceeding.
- **Incremental**: Add stories in order P1 -> P2 -> P3.
