# This file defines the contract that every handler must follow.
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.chatbot.session_manager import SessionManager


class BaseHandler(ABC):

    def __init__(self, db: Session):
        self.db = db
        self.session_manager = SessionManager(db)

    @abstractmethod
    def handle(
        self,
        customer,
        session,
        message: str
    ) -> str:
        """
        Process the user's message and return the bot response.
        """
        pass
