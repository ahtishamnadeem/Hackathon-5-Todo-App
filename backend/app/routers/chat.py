"""Chat API router for AI agent integration."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from sqlmodel import Session
from ..database import get_session
from ..middleware.auth import get_current_user
from ..models.user import User
from ..agents.agent_runner import AgentRunner

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None


@router.post("/{user_id}/chat", response_model=ChatResponse)
def chat_endpoint(
    user_id: int,
    request: ChatRequest,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    Process a natural language message from a user and return an AI-generated response
    with any tool invocations that occurred.

    Args:
        user_id: The ID of the user making the request (from URL path)
        request: Contains the conversation_id (optional) and message content
        current_user_id: The authenticated user ID (from JWT token)
        db: Database session

    Returns:
        ChatResponse with success status, data (including conversation_id, response, and tool_calls), and error info
    """
    # Verify that the user_id in the URL matches the authenticated user
    if current_user_id != user_id:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized: user_id in URL does not match authenticated user"
        )

    # Initialize the agent runner
    agent_runner = AgentRunner()

    # Run the chat request
    result = agent_runner.run_chat_request(
        user_id=user_id,
        message_content=request.message,
        conversation_id=request.conversation_id
    )

    return result