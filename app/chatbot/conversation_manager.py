from sqlalchemy.orm import Session

from app.chatbot.router import ConversationRouter
from app.chatbot.states import ChatState
# from app.chatbot.prompts import NEW_CUSTOMER
from app.chatbot.prompts import MAIN_MENU
from app.chatbot.session_manager import SessionManager
from app.ai.graph.service import RestaurantGraphService
from app.services.customer_service import (
    get_customer_by_telegram_id
)


class ConversationManager:

    def __init__(self, db: Session):

        self.db = db

        self.router = ConversationRouter(db)

        self.session_manager = SessionManager(db)

        self.graph = RestaurantGraphService(db)

    def start_conversation(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str
    ):
        customer = get_customer_by_telegram_id(
            self.db,
            telegram_id
        )

        if customer:
            session = self.session_manager.get_or_create(
                customer.customer_id
            )

            self.session_manager.set_state(
                session, ChatState.MAIN_MENU.value)

            return (
                f"Welcome back, {customer.first_name}! 😊\n\n"
                f"{MAIN_MENU}"
            )

        return "REGISTER"

    def handle_message(
        self,
        telegram_id: int,
        message: str
    ):

        customer = get_customer_by_telegram_id(
            self.db,
            telegram_id
        )
        print("Customer:", customer)

        # new customer
        if customer is None:
            print("Customer not found")
            return (
                "Please use /start to begin registration."

            )
        session = self.session_manager.get_or_create(
            customer.customer_id
        )
        print("=" * 50)
        print("Session State:", session.current_state)
        print("Session Context:", session.context)
        print("=" * 50)
        graph = RestaurantGraphService(self.db)

        # return self.router.route(
        #     customer=customer,
        #     session=session,
        #     message=message
        # )

        return self.graph.run(
            customer_id=customer.customer_id,
            user_message=message,
        )
