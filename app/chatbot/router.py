# This file decides which handler should process the next message.

from sqlalchemy.orm import Session

from app.chatbot.registery_handler import HandlerRegistry


class ConversationRouter:

    def __init__(self, db: Session):

        self.registry = HandlerRegistry(db)

    def route(
        self,
        customer,
        session,
        message: str
    ) -> str:

        handler = self.registry.get_handler(
            session.current_state
        )

        if handler is None:

            return (
                "Sorry, I couldn't understand your request."
            )

        return handler.handle(
            customer=customer,
            session=session,
            message=message
        )
