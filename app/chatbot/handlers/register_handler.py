from sqlalchemy.orm import Session

from app.chatbot.handlers.base_handler import BaseHandler
from app.chatbot.prompts import MAIN_MENU, NEW_CUSTOMER
from app.chatbot.states import ChatState

from app.services.customer_service import (
    check_customer,
    link_existing_customer,
    register_telegram_customer
)

from app.services.chatbot_session_service import (
    start_session,
    change_state
)


class RegisterHandler(BaseHandler):

    def __init__(self, db: Session):
        super().__init__(db)

    def handle(
        self,
        customer,
        session,
        message: str
    ) -> str:
        return NEW_CUSTOMER

    def register_contact(
        self,
        telegram_id: int,
        username: str | None,
        first_name: str,
        phone: str
    ):

        print("========== REGISTER CONTACT ==========")
        print("Telegram ID:", telegram_id)
        print("Username:", username)
        print("First Name:", first_name)
        print("Phone:", phone)

        customer = self._find_or_create_customer(
            telegram_id,
            username,
            first_name,
            phone
        )

        self._create_session(
            customer.customer_id
        )

        return self._show_main_menu(
            customer.first_name
        )

    def _find_or_create_customer(
        self,
        telegram_id,
        username,
        first_name,
        phone
    ):

        print("Checking phone:", phone)

        result = check_customer(
            self.db,
            phone
        )

        print("Customer exists:", result["exists"])
        print("Customer object:", result["customer"])

        # Existing customer
        if result["exists"]:

            print("✅ Existing customer found")
            print("Customer ID:", result["customer"].customer_id)

            customer = link_existing_customer(
                db=self.db,
                customer=result["customer"],
                telegram_id=telegram_id,
                username=username
            )

            print("Telegram ID linked:", customer.telegram_id)

            return customer

        # New customer
        print("🆕 Creating new customer...")

        customer = register_telegram_customer(
            db=self.db,
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            phone=phone
        )

        print("Created Customer ID:", customer.customer_id)
        print("Created Telegram ID:", customer.telegram_id)

        return customer

    def _create_session(
        self,
        customer_id: int
    ):

        session = start_session(
            self.db,
            customer_id
        )

        change_state(
            self.db,
            session,
            ChatState.MAIN_MENU.value
        )

        return session

    def _show_main_menu(
        self,
        first_name: str
    ):

        return (
            f"✅ Registration Successful!\n\n"
            f"Welcome {first_name}! 😊\n\n"
            f"{MAIN_MENU}"
        )
