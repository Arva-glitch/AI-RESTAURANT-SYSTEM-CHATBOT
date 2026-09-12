from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.chatbot_conversation import ChatBotConversation


chatbot_conversation_crud = CRUDBase(
    ChatBotConversation
)


def get_conversation_history(
    db: Session,
    customer_id: int
):

    return (
        db.query(ChatBotConversation)
        .filter(
            ChatBotConversation.customer_id ==
            customer_id
        )
        .order_by(
            ChatBotConversation.created_at.asc()
        )
        .all()
    )


def get_recent_conversations(
    db: Session,
    customer_id: int,
    limit: int = 20
):

    return (
        db.query(ChatBotConversation)
        .filter(
            ChatBotConversation.customer_id ==
            customer_id
        )
        .order_by(
            ChatBotConversation.created_at.desc()
        )
        .limit(limit)
        .all()
    )
