from sqlalchemy.orm import Session

from app.models.chatbot_session import ChatBotSession
from app.schemas.chatbot_session import (
    ChatBotSessionCreate,
    ChatBotSessionUpdate
)


def create_session(
    db: Session,
    session: ChatBotSessionCreate
):
    db_session = ChatBotSession(**session.model_dump())

    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session


def get_active_session(
    db: Session,
    customer_id: int
):
    return (
        db.query(ChatBotSession)
        .filter(
            ChatBotSession.customer_id == customer_id,
            ChatBotSession.is_active == 1
        )
        .first()
    )


def update_session(
    db: Session,
    session: ChatBotSession,
    update_data: ChatBotSessionUpdate
):

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(session, key, value)

    db.commit()
    db.refresh(session)

    return session


def close_session(
    db: Session,
    session: ChatBotSession
):

    session.is_active = 0

    db.commit()
    db.refresh(session)

    return session


def delete_session(
    db: Session,
    session: ChatBotSession
):
    db.delete(session)
    db.commit()
