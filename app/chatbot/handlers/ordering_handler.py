from sqlalchemy.orm import Session

from app.chatbot.handlers.base_handler import BaseHandler


class OrderingHandler(BaseHandler):

    def __init__(self, db: Session):
        super().__init__(db)

    def handle(
        self,
        customer,
        session,
        message: str
    ) -> str:

        return "🍕 Online ordering flow will start here."
