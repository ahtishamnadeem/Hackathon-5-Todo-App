# Data Model: Conversational Chat UI

## Overview
This document describes the data entities and relationships required for the conversational chat interface. The chat UI consumes data from the existing backend entities (User, Todo) and interacts with the new MCP tools for task management. The frontend maintains minimal state, relying on the backend for conversation persistence.

## Entity Relationships

```
User (1) -----> (Many) Todo
User (1) -----> (Many) Conversation
Conversation (1) -----> (Many) Message
```

## Entity Definitions

### User (Existing from Phase II)
**Purpose**: Represents the authenticated user interacting with the chat interface, validated through JWT token

**Fields**:
- id: Integer (Primary Key)
- email: String (Unique, NOT NULL)
- password_hash: String (NOT NULL)
- created_at: DateTime (NOT NULL)
- updated_at: DateTime (NOT NULL)

**Validation Rules**:
- Email must be unique
- Proper JWT authentication required for access
- User identity verified through backend authentication

**Relationships**:
- Owns many Todos (one-to-many)
- Owns many Conversations (one-to-many)
- Owns many Messages through Conversations (indirect one-to-many)

### Todo (Existing from Phase II)
**Purpose**: Represents task items that can be managed through natural language commands via the AI agent

**Fields**:
- id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User, NOT NULL)
- title: String (NOT NULL, max 500 characters)
- description: Text (Optional)
- completed: Boolean (Default False)
- created_at: DateTime (NOT NULL)
- updated_at: DateTime (NOT NULL)

**Validation Rules**:
- user_id must reference an existing User
- Title cannot be empty
- completed defaults to False
- All queries must be scoped to authenticated user_id

**Relationships**:
- Belongs to one User (many-to-one)
- User can access only their own todos (enforced by backend)

### Conversation (New for Phase III)
**Purpose**: Represents a user's chat session with the AI assistant, containing metadata and linking to associated messages

**Fields**:
- id: Integer (Primary Key, Auto-increment)
- user_id: Integer (Foreign Key to User, NOT NULL)
- title: String (Optional, max 255 characters)
- created_at: DateTime (NOT NULL, default now)
- updated_at: DateTime (NOT NULL, default now, auto-update)

**Validation Rules**:
- user_id must reference an existing User
- created_at and updated_at automatically managed by database
- Title is optional and limited to 255 characters

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many, cascade delete)

### Message (New for Phase III)
**Purpose**: Represents individual exchanges between user and AI, including role (user/assistant), content, and timestamp

**Fields**:
- id: Integer (Primary Key, Auto-increment)
- conversation_id: Integer (Foreign Key to Conversation, NOT NULL)
- role: String (Enum: "user", "assistant", "system", NOT NULL)
- content: Text (NOT NULL)
- timestamp: DateTime (NOT NULL, default now)

**Validation Rules**:
- conversation_id must reference an existing Conversation
- role must be one of "user", "assistant", or "system"
- content cannot be empty
- timestamp automatically set when record is created

**Relationships**:
- Belongs to one Conversation (many-to-one)
- Linked to User through Conversation (indirect many-to-one)

## State Transitions

### Todo State Transitions
- New Todo: completed = False (default)
- Complete Todo: completed = True
- Uncomplete Todo: completed = False

### Message Role Transitions
- "user" (messages sent by the user)
- "assistant" (responses from the AI agent)
- "system" (internal system messages, if needed)

## Data Integrity Constraints

### Foreign Key Constraints
- All foreign keys enforce referential integrity
- Prevent orphaned records through foreign key constraints
- Cascade delete on Conversation -> Messages relationship

### User Isolation
- All queries must filter by user_id to maintain isolation
- Cross-user data access prevented by backend authentication
- Tools verify user ownership before operations

## Indexes

### Existing Indexes (from Todo/User models)
- Index on Todo.user_id for performance (critical for user isolation)
- Index on User.email for authentication performance

### New Indexes (for Conversation/Message models)
- Index on Conversation.user_id for performance
- Index on Message.conversation_id for message loading
- Index on Message.timestamp for chronological ordering

## API Contract Data Structures

### Chat Request Payload
```json
{
  "conversation_id": {
    "type": "integer",
    "required": false,
    "description": "ID of existing conversation. If omitted, a new conversation will be created."
  },
  "message": {
    "type": "string",
    "required": true,
    "description": "The user's message to the AI assistant",
    "maxLength": 10000
  }
}
```

### Chat Response Payload
```json
{
  "success": {
    "type": "boolean",
    "value": true
  },
  "data": {
    "conversation_id": {
      "type": "integer",
      "description": "ID of the conversation (newly created or existing)"
    },
    "response": {
      "type": "string",
      "description": "AI-generated response to the user's message"
    },
    "tool_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "Name of the MCP tool that was called"
          },
          "arguments": {
            "type": "object",
            "description": "Arguments passed to the tool"
          },
          "result": {
            "type": "object",
            "description": "Result returned by the tool"
          }
        }
      },
      "description": "Array of MCP tools that were invoked during processing"
    }
  },
  "error": {
    "type": null
  }
}
```

### Message Display Object (Frontend)
```json
{
  "id": {
    "type": "number",
    "description": "Unique identifier (from backend)"
  },
  "role": {
    "type": "'user' | 'assistant'",
    "description": "Who sent the message"
  },
  "content": {
    "type": "string",
    "description": "Message content"
  },
  "timestamp": {
    "type": "Date",
    "description": "When message was created"
  },
  "isLoading": {
    "type": "boolean",
    "description": "For assistant messages during processing (frontend only)",
    "required": false
  }
}
```

## Performance Considerations

### Query Optimization for Chat Operations
- Most frequent query: Load user's conversation history by user_id (already indexed)
- Second most frequent: Load specific conversation by conversation_id with user_id check
- Third most frequent: Load messages by conversation_id with timestamp ordering
- Index strategy: Primary indexes on all foreign key relationships (existing and new)

### Pagination Strategy
- Implement pagination for conversation history to handle large volumes
- Default page size: 50 messages per page
- Support for infinite scrolling in UI
- Efficient database queries with proper indexing