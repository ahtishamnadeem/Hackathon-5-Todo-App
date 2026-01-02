# Data Model: Phase I Todo

## Entities

### Todo
Represents a single task in the system.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| id | int | Unique identifier | Must be > 0 |
| title | str | Task description | Max 255 chars, not empty |
| completed | bool | Status flag | Default: False |

## State Transitions
- **Created**: Status is `completed=False`.
- **Completed**: Status set to `True`.
- **Updated**: Title can be changed at any time.
- **Deleted**: Removed from the in-memory pool.
