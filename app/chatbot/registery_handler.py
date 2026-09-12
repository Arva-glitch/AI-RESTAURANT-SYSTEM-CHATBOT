from app.chatbot.states import ChatState
from sqlalchemy.orm import Session
from app.chatbot.handlers.register_handler import RegisterHandler
from app.chatbot.handlers.main_menu_handler import MainMenuHandler
from app.chatbot.handlers.booking_handler import BookingHandler
from app.chatbot.handlers.ordering_handler import OrderingHandler


class HandlerRegistry:

    def __init__(self, db: Session):
        booking_handler = BookingHandler(db)
        ordering_handler = OrderingHandler(db)

        self.handlers = {

            ChatState.REGISTER.value:
                RegisterHandler(db),

            ChatState.MAIN_MENU.value:
                MainMenuHandler(db),

            ChatState.BOOKING_DATE.value:
                booking_handler,

            ChatState.BOOKING_TIME.value:
                booking_handler,

            ChatState.BOOKING_GUESTS.value:
                booking_handler,

            ChatState.BOOKING_CONFIRMATION.value:
                booking_handler,


            ChatState.ORDERING.value:
                ordering_handler,

            # ChatState.REVIEW.value:
            #     ReviewHandler(db)


        }

    def get_handler(
        self,
        state: str
    ):

        return self.handlers.get(state)
