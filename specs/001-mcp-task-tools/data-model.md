# Data Model: MCP Server & Task Tools

## Overview
This document describes the data entities and relationships required for the MCP server and task management tools. The data model leverages the existing Todo application data model while extending it for MCP tool requirements.

## Entity Relationships

```
User (1) -----> (Many) Todo
```

Note: The MCP tools will operate on the existing Todo entity rather than creating new entities, ensuring consistency with the existing data model.

## Entity Definitions

### Task (Reusing existing Todo entity)
**Purpose**: Represents a todo item that can be managed through MCP tools, with id, title, description, completion status, user association, and timestamps

**Fields** (from existing Todo model):
- id: Integer (Primary Key, Auto-increment)
- user_id: Integer (Foreign Key to User, NOT NULL)
- title: String (NOT NULL, max 500 characters)
- description: Text (Optional)
- completed: Boolean (Default False)
- created_at: DateTime (NOT NULL, default now)
- updated_at: DateTime (NOT NULL, default now, auto-update)

**Validation Rules** (from existing Todo model):
- user_id must reference an existing User
- Title cannot be empty
- completed defaults to False
- created_at and updated_at automatically managed by database

**Relationships** (from existing Todo model):
- Belongs to one User (many-to-one)
- Linked to User through user_id foreign key

### User (Existing from Phase II)
**Purpose**: Represents the owner of tasks, referenced by user_id in all operations for access control

**Fields**:
- id: Integer (Primary Key, Auto-increment)
- email: String (Unique, NOT NULL)
- password_hash: String (NOT NULL)
- created_at: DateTime (NOT NULL, default now)
- updated_at: DateTime (NOT NULL, default now, auto-update)

**Validation Rules**:
- Email must be unique
- Password must be properly hashed
- Email follows standard validation patterns

## MCP Tool Data Contracts

### add_task Tool Contract
**Input Parameters**:
- user_id: Integer (required) - ID of the user creating the task
- title: String (required) - Title of the task
- description: String (optional) - Description of the task

**Output**:
- success: Boolean (true if successful)
- data: Object containing:
  - id: Integer (ID of the created task)
  - status: String ("created")
  - title: String (title of the created task)
- error: Object (if failure)

### list_tasks Tool Contract
**Input Parameters**:
- user_id: Integer (required) - ID of the user whose tasks to retrieve
- status: String (optional) - Filter by completion status ("all", "pending", "completed")

**Output**:
- success: Boolean (true if successful)
- data: Array of Objects containing:
  - id: Integer (task ID)
  - title: String (task title)
  - completed: Boolean (completion status)
- error: Object (if failure)

### complete_task Tool Contract
**Input Parameters**:
- user_id: Integer (required) - ID of the user
- task_id: Integer (required) - ID of the task to update

**Output**:
- success: Boolean (true if successful)
- data: Object containing:
  - task_id: Integer (ID of the updated task)
  - status: String ("completed")
  - title: String (title of the updated task)
- error: Object (if failure)

### update_task Tool Contract
**Input Parameters**:
- user_id: Integer (required) - ID of the user
- task_id: Integer (required) - ID of the task to update
- title: String (optional) - New title for the task
- description: String (optional) - New description for the task

**Output**:
- success: Boolean (true if successful)
- data: Object containing:
  - task_id: Integer (ID of the updated task)
  - status: String ("updated")
  - title: String (title of the updated task)
- error: Object (if failure)

### delete_task Tool Contract
**Input Parameters**:
- user_id: Integer (required) - ID of the user
- task_id: Integer (required) - ID of the task to delete

**Output**:
- success: Boolean (true if successful)
- data: Object containing:
  - task_id: Integer (ID of the deleted task)
  - status: String ("deleted")
  - title: String (title of the deleted task)
- error: Object (if failure)

## Indexes

### Existing Indexes (from Todo model)
- Index on Todo.user_id for performance (critical for user isolation)
- Index on User.email for authentication performance

### Recommended Indexes for MCP Operations
- Composite index on (Todo.user_id, Todo.created_at) for list_tasks sorting
- Index on Todo.completed for status filtering operations

## State Transitions

### Task State Transitions
- New Task: completed = False (default)
- Complete Task: completed = True
- Uncomplete Task: completed = False
- Update Task: title/description modified
- Delete Task: record removed

## Data Integrity Constraints

### Existing Constraints (from Todo model)
- All foreign keys enforce referential integrity
- user_id must reference an existing User
- Prevent orphaned records through foreign key constraints

### MCP Tool Constraints
- All operations must validate user_id ownership before execution
- Tools must not allow cross-user data access
- All operations must maintain data consistency

## Performance Considerations

### Query Optimization for MCP Tools
- Most frequent query: Load user's tasks by user_id (already indexed)
- Second most frequent: Load specific task by task_id and user_id
- Filtering operations: Status-based queries on completed field
- Sorting operations: Creation time ordering (uses created_at index)

### Index Strategy
- Primary indexes on all foreign key relationships (existing)
- Additional indexes on frequently queried columns for MCP operations
- Optimize for read-heavy task list operations
- Support efficient filtering and sorting for list_tasks tool