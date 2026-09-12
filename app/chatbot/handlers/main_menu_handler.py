from sqlalchemy.orm import Session

from app.chatbot.handlers.base_handler import BaseHandler
from app.chatbot.states import ChatState

from app.services.chatbot_session_service import change_state


class MainMenuHandler(BaseHandler):

    def __init__(self, db: Session):
        super().__init__(db)

    def handle(
        self,
        customer,
        session,
        message: str
    ) -> str:

        if message == "🍽️ Book Table":

            change_state(
                self.db,
                session,
                ChatState.BOOKING_DATE.value
            )

            return (
                "📅 Great!\n\n"
                "Please enter your booking date.\n\n"
                "Example:\n"
                "25-07-2026"
            )

        if message == "🛵 Order Online":

            change_state(
                self.db,
                session,
                ChatState.ORDERING.value
            )

            return (
                "🍕 Awesome!\n\n"
                "Would you like Delivery or Pickup?"
            )

        if message == "📖 View Menu":

            return (
                "📖 Menu feature coming next..."
            )

        if message == "🎁 Offers":

            return (
                "🎁 Offers feature coming next..."
            )

        if message == "⭐ Reviews":

            return (
                "⭐ Review feature coming next..."
            )

        return (
            "Please choose an option using the buttons below."
        )
