# Quickstart Guide: MCP Server & Task Tools

## Overview
This guide provides instructions for setting up and using the MCP (Model Context Protocol) server with task management tools for the AI agent system.

## Prerequisites

### System Requirements
- Python 3.13+
- PostgreSQL database (PostgreSQL 13 or higher)
- Official MCP SDK
- SQLModel for database operations

### Environment Setup
1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   ```

## MCP Server Setup

### Initialize the MCP Server
1. The MCP server is implemented as part of the existing backend application
2. The server follows the stateless-by-design architecture principle
3. All tools operate through the existing database layer using SQLModel

### Available MCP Tools
The following MCP-compliant tools are available for AI agent integration:

1. **add_task**: Create new todo tasks
2. **list_tasks**: Retrieve user's tasks with optional filtering
3. **complete_task**: Mark tasks as completed
4. **update_task**: Modify task properties
5. **delete_task**: Remove tasks permanently

## Using the MCP Tools

### Tool Invocation
Each MCP tool follows the same invocation pattern with consistent response format:

**Request Format**:
```json
{
  "user_id": 123,
  "parameters": {
    // tool-specific parameters
  }
}
```

**Success Response Format**:
```json
{
  "success": true,
  "data": {
    // tool-specific result data
  },
  "error": null
}
```

**Error Response Format**:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {}
  }
}
```

### Tool-Specific Usage

#### add_task
Create a new task:
```
Parameters:
- user_id (required): ID of the user
- title (required): Title of the task
- description (optional): Description of the task

Returns:
- task ID, status, and title
```

#### list_tasks
Retrieve tasks for a user:
```
Parameters:
- user_id (required): ID of the user
- status (optional): Filter by status ("all", "pending", "completed")

Returns:
- Array of task objects (id, title, completed)
```

#### complete_task
Mark a task as completed:
```
Parameters:
- user_id (required): ID of the user
- task_id (required): ID of the task

Returns:
- task ID, status, and title
```

#### update_task
Modify task properties:
```
Parameters:
- user_id (required): ID of the user
- task_id (required): ID of the task
- title (optional): New title
- description (optional): New description

Returns:
- task ID, status, and title
```

#### delete_task
Remove a task:
```
Parameters:
- user_id (required): ID of the user
- task_id (required): ID of the task

Returns:
- task ID, status, and title
```

## Security Configuration

### User Isolation
- All tools enforce user isolation by validating user_id ownership
- Cross-user data access is prevented
- Unauthorized access attempts return appropriate error codes

### Error Handling
- All tools return structured error responses
- Validation errors are clearly communicated
- Database errors are handled gracefully

## Integration with AI Agent

### Calling MCP Tools from AI Agent
The AI agent can invoke MCP tools by calling the appropriate functions with validated parameters. The tools are designed to be deterministic and machine-readable for AI consumption.

### Sample Integration
```python
# Example of how AI agent might use MCP tools
result = mcp_tools.add_task(
    user_id=123,
    title="Buy groceries",
    description="Milk, eggs, bread"
)

if result["success"]:
    print(f"Task created: {result['data']['title']}")
else:
    print(f"Error: {result['error']['message']}")
```

## Testing

### Unit Tests
Run unit tests for MCP tools:
```
pytest tests/unit/mcp_tools/
```

### Integration Tests
Test MCP tool integration:
```
pytest tests/integration/mcp_integration/
```

### Contract Tests
Validate MCP tool contracts:
```
pytest tests/contract/mcp_contracts/
```

## Configuration

### Database Settings
The MCP tools use the same database configuration as the rest of the application. Ensure your DATABASE_URL is properly configured in environment variables.

### Performance Tuning
- Tools are designed to execute within 2 seconds
- Database indexes are optimized for common operations
- Connection pooling is handled by the existing infrastructure

## Troubleshooting

### Common Issues
1. **Permission Denied**: Verify user_id matches the resource owner
2. **Resource Not Found**: Check that the requested resource exists
3. **Validation Error**: Ensure all required parameters are provided with correct types
4. **Database Connection**: Verify database connectivity and credentials

### Logging
MCP tool operations are logged for debugging and monitoring. Check application logs for detailed information about tool execution.

## Next Steps

1. Integrate MCP tools with the AI agent system
2. Test tool reliability and error handling
3. Monitor performance under load
4. Validate security controls