# Data Model: AI Agent & Conversation System

## Overview
This document describes the data entities required for the AI-powered todo chatbot with agentic architecture and MCP integration.

## Entity Relationships

```
User (1) -----> (Many) Todo
User (1) -----> (Many) Conversation
Conversation (1) -----> (Many) Message
```

## Entity Definitions

### Conversation
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

### Message
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

### User (Existing from Phase II)
**Purpose**: Represents authenticated users with todo management capabilities

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

### Todo (Existing from Phase II)
**Purpose**: Represents user tasks that can be managed through natural language commands

**Fields**:
- id: Integer (Primary Key, Auto-increment)
- user_id: Integer (Foreign Key to User, NOT NULL)
- title: String (NOT NULL, max 255 characters)
- description: Text (Optional)
- completed: Boolean (Default False)
- created_at: DateTime (NOT NULL, default now)
- updated_at: DateTime (NOT NULL, default now, auto-update)

**Validation Rules**:
- user_id must reference an existing User
- Title cannot be empty
- completed defaults to False

## Indexes

- Index on User.user_id for performance
- Index on Todo.user_id for performance
- Index on Conversation.user_id for performance
- Index on Message.conversation_id for performance
- Index on Message.timestamp for chronological ordering

## State Transitions

### Todo State Transitions
- New Todo: completed = False (default)
- Toggle Complete: completed = !completed (can go back and forth)

### Message Role Transitions
- "user" (messages sent by the user)
- "assistant" (responses from the AI agent)
- "system" (internal system messages, if needed)

## Data Integrity Constraints

### Foreign Key Constraints
- All foreign keys enforce referential integrity
- Cascade delete on Conversation -> Messages relationship
- Prevent orphaned records

### User Isolation
- All queries must filter by user_id to maintain isolation
- No cross-user data access allowed
- JWT validation ensures proper user context

## Migration Requirements

### New Tables
1. `conversations` table with indexes on user_id
2. `messages` table with indexes on conversation_id and timestamp

### Existing Table Updates
- No changes needed to existing User and Todo tables
- Maintain all existing constraints and indexes

## Performance Considerations

### Query Optimization
- Most frequent query: Load conversation history by conversation_id
- Second most frequent: Load all conversations for a user
- Message queries will be filtered by conversation_id and ordered by timestamp

### Index Strategy
- Primary indexes on all foreign key relationships
- Additional indexes on frequently queried columns
- Optimize for read-heavy conversation history access