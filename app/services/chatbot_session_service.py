from sqlalchemy.orm import Session

from app.crud.chatbot_session import (
    create_session,
    get_active_session,
    update_session,
    close_session
)

from app.schemas.chatbot_session import (
    ChatBotSessionCreate,
    ChatBotSessionUpdate
)


def start_session(
    db: Session,
    customer_id: int
):
    """
    Start a new chatbot session.
    """

    session = get_active_session(
        db,
        customer_id
    )

    if session:
        return session

    return create_session(
        db,
        ChatBotSessionCreate(
            customer_id=customer_id,
            current_state="MAIN_MENU",
            current_intent=None,
            context={}
        )
    )


def fetch_active_session(
    db: Session,
    customer_id: int
):
    return get_active_session(
        db,
        customer_id
    )


def change_state(
    db: Session,
    session,
    new_state: str
):

    return update_session(
        db,
        session,
        ChatBotSessionUpdate(
            current_state=new_state
        )
    )


def change_intent(
    db: Session,
    session,
    intent: str
):

    return update_session(
        db,
        session,
        ChatBotSessionUpdate(
            current_intent=intent
        )
    )


def update_context(
    db: Session,
    session,
    context: dict
):

    return update_session(
        db,
        session,
        ChatBotSessionUpdate(
            context=context
        )
    )


def end_session(
    db: Session,
    session
):

    return close_session(
        db,
        session
    )
