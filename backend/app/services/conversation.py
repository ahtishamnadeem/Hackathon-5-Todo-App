from typing import List, Optional
from sqlmodel import Session, select
from ..models.conversation import Conversation, ConversationCreate
from ..models.user import User
from ..database import engine


class ConversationService:
    """
    Service for managing conversations with proper user isolation and security.
    """

    @staticmethod
    def create_conversation(conversation_create: ConversationCreate) -> Optional[Conversation]:
        """
        Create a new conversation for a user.

        Args:
            conversation_create: Data for creating the conversation

        Returns:
            Created Conversation object or None if failed
        """
        with Session(engine) as session:
            # Verify user exists
            user = session.get(User, conversation_create.user_id)
            if not user:
                return None

            conversation = Conversation.model_validate(conversation_create)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation

    @staticmethod
    def get_conversation_by_id(conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for a user (enforcing user isolation).

        Args:
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user requesting the conversation

        Returns:
            Conversation object if it belongs to the user, None otherwise
        """
        with Session(engine) as session:
            conversation = session.get(Conversation, conversation_id)
            if conversation and conversation.user_id == user_id:
                return conversation
            return None

    @staticmethod
    def get_conversations_by_user(user_id: int) -> List[Conversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List of Conversation objects belonging to the user
        """
        with Session(engine) as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            conversations = session.exec(statement).all()
            return conversations

    @staticmethod
    def update_conversation(conversation_id: int, user_id: int, title: Optional[str]) -> Optional[Conversation]:
        """
        Update a conversation for a user (enforcing user isolation).

        Args:
            conversation_id: ID of the conversation to update
            user_id: ID of the user requesting the update
            title: New title for the conversation (optional)

        Returns:
            Updated Conversation object if successful, None otherwise
        """
        with Session(engine) as session:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                return None

            if title is not None:
                conversation.title = title
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            return conversation

    @staticmethod
    def delete_conversation(conversation_id: int, user_id: int) -> bool:
        """
        Delete a conversation for a user (enforcing user isolation).

        Args:
            conversation_id: ID of the conversation to delete
            user_id: ID of the user requesting the deletion

        Returns:
            True if successful, False otherwise
        """
        with Session(engine) as session:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                return False

            session.delete(conversation)
            session.commit()
            return True