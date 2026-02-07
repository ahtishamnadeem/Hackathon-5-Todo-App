# Quickstart Guide: Conversational Chat UI

## Overview
This guide provides instructions for setting up and using the conversational chat interface that allows authenticated users to manage their todo tasks through natural language with an AI assistant.

## Prerequisites

### System Requirements
- Node.js 18+ (for frontend development)
- Python 3.13+ (for backend API)
- PostgreSQL database (Phase II backend must be running)
- OpenAI API key for AI agent functionality
- Better Auth configured for authentication

### Environment Setup
1. Install Node.js dependencies:
   ```
   cd frontend
   npm install
   ```

2. Install Python dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   # Backend (.env)
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   SECRET_KEY=your_secret_key_for_jwt
   ```

## Running the Application

### Backend Setup
1. Ensure the Phase II backend is running with MCP tools:
   ```
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

2. Verify the chat endpoint is available at:
   - `POST /api/{user_id}/chat`

### Frontend Setup
1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Start the development server:
   ```
   npm run dev
   ```

3. The chat interface will be available at `http://localhost:3000/chat`

## Using the Chat Interface

### Authentication
1. Users must be logged in to access the chat interface
2. The application uses Better Auth for authentication
3. JWT tokens are automatically included in API requests

### Starting a Conversation
1. Navigate to the chat interface
2. Begin typing a natural language command such as:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark the first task as completed"

### Continuing a Conversation
1. The conversation_id is automatically stored in session storage
2. Subsequent messages will continue the same conversation
3. Page refreshes maintain conversation continuity

## API Integration

### Making Chat Requests
The frontend communicates with the backend through the chat API:

**Request Format**:
```
POST /api/{user_id}/chat
Authorization: Bearer {jwt_token}
Content-Type: application/json

{
  "conversation_id": 123,  // Optional - omit for new conversation
  "message": "Add a task to buy groceries"
}
```

**Response Format**:
```
{
  "success": true,
  "data": {
    "conversation_id": 123,
    "response": "I've added the task 'buy groceries' to your list.",
    "tool_calls": [...]
  },
  "error": null
}
```

## Development

### Running Tests
1. Frontend tests:
   ```
   npm run test
   ```

2. Backend tests:
   ```
   pytest tests/
   ```

### Adding New Features
1. Follow the existing component structure in `frontend/app/chat/components/`
2. Use the existing hooks pattern in `frontend/app/chat/hooks/`
3. Follow accessibility guidelines for chat interfaces
4. Ensure responsive design across all screen sizes

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Ensure JWT token is properly set and not expired
2. **API Connection**: Verify backend is running and accessible at configured URL
3. **Conversation Continuity**: Check that conversation_id is being properly stored and reused
4. **AI Agent Not Responding**: Verify OpenAI API key is valid and has sufficient quota

### Logging
- Frontend: Console logs for UI state and API interactions
- Backend: Standard logging for API requests and AI agent interactions
- Monitor both for debugging conversation flow issues

## Next Steps

1. Test the chat interface with various natural language commands
2. Verify conversation continuity across page reloads
3. Test responsive behavior on different screen sizes
4. Validate security by ensuring proper user isolation
5. Performance test with extended conversations