# Quickstart Guide: AI Agent & Conversation System

## Overview
This guide provides instructions for setting up and running the AI-powered todo chatbot with agentic architecture and MCP integration.

## Prerequisites

### System Requirements
- Python 3.13+
- PostgreSQL database (PostgreSQL 13 or higher)
- OpenAI API key
- MCP SDK (if implementing MCP tools)

### Environment Setup
1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   SECRET_KEY=your_secret_key_for_jwt
   ```

## Database Setup

### Schema Migration
1. Run database migrations to create new tables:
   ```
   alembic upgrade head
   ```

2. Verify new tables exist:
   - conversations table
   - messages table
   - Existing user and todo tables remain unchanged

## Running the Service

### Start the Backend
1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

3. The service will be available at `http://localhost:8000`

## API Usage

### Authentication
All chat endpoints require JWT authentication. Obtain a token through the existing authentication endpoints:
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "user_password"
}
```

### Chat Endpoint
Send a message to the AI assistant:
```
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

### Starting a New Conversation
Omit the conversation_id to start a new conversation:
```
POST /api/123/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

### Continuing a Conversation
Include conversation_id to continue an existing conversation:
```
POST /api/123/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "conversation_id": 456,
  "message": "Show me my tasks"
}
```

## Configuration

### OpenAI Agent Settings
The AI agent can be configured via environment variables:
- `OPENAI_MODEL`: Model to use (default: gpt-4-turbo)
- `AGENT_TEMPERATURE`: Creativity level (default: 0.7)

### MCP Tool Configuration
MCP tools are registered automatically when the service starts. Available tools:
- `add_task`: Creates a new todo item
- `list_tasks`: Retrieves user's todo items
- `complete_task`: Marks a todo as completed
- `delete_task`: Removes a todo item
- `update_task`: Modifies a todo item

## Development

### Running Tests
1. Unit tests:
   ```
   pytest tests/unit/
   ```

2. Integration tests:
   ```
   pytest tests/integration/
   ```

3. Contract tests:
   ```
   pytest tests/contract/
   ```

### Adding New MCP Tools
1. Create a new tool in `backend/app/mcp_tools/`
2. Register the tool with the agent in `backend/app/agents/todo_agent.py`
3. Ensure the tool follows the MCP tool conventions:
   - Stateless execution
   - User_id validation
   - Proper error handling
   - Structured responses

## Troubleshooting

### Common Issues
1. **Invalid JWT Token**: Ensure the token is properly formatted and not expired
2. **Database Connection**: Verify DATABASE_URL is correct and database is accessible
3. **OpenAI API Error**: Check that OPENAI_API_KEY is valid and has sufficient quota
4. **Conversation Not Found**: Verify conversation belongs to the authenticated user

### Logging
Service logs are available in the console output. Enable debug logging by setting:
```
LOG_LEVEL=debug
```

## Next Steps

1. Test the chat functionality with various natural language commands
2. Verify conversation persistence across server restarts
3. Test user isolation to ensure cross-user access prevention
4. Validate MCP tool execution and error handling