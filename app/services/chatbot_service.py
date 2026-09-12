from sqlalchemy.orm import Session
from app.services.intent_service import detect_intent, Intent
from app.services.intent_service import (
    detect_intent,
    Intent
)

from app.services.user_history_service import (
    log_activity
)

from app.crud.chatbot_conversation import (
    chatbot_conversation_crud
)

from app.schemas.chatbot_conversation import (
    ChatBotConversationCreate
)
# -------------------saving conversation------------------------------------------------------------


def save_conversation(
    db: Session,
    customer_id: int,
    user_message: str,
    bot_response: str,
    detected_intent: str
):

    conversation = ChatBotConversationCreate(

        customer_id=customer_id,

        user_message=user_message,

        bot_response=bot_response,

        detected_intent=detected_intent

    )

    return chatbot_conversation_crud.create(
        db,
        conversation
    )

# -------------------------------main chatbot function---------------------------------------------


def process_message(
    db: Session,
    customer_id: int,
    message: str
):

    intent = detect_intent(message)

# ----------------------------------booking----------------------------------------------------------
    if intent == Intent.BOOK_TABLE:

        response = (
            "Sure! I'll help you book a table."
        )

        # Later:
        # response = booking_service.book_table(...)
# -------------------------------------ordering-----------------------------------------------------
    elif intent == Intent.ORDER_ONLINE:

        response = (
            "Sure! Let's place your order."
        )

        # Later:
        # response = order_service.place_order(...)
# ------------------------------------------menu---------------------------------------------------
    elif intent == Intent.VIEW_MENU:
        response = (
            "I'll show you today's menu."
        )

        # Later:
        # response = menu_service.get_menu(...)

# ------------------payments-----------------------------------------------------------
    elif intent == Intent.PAYMENT:

        response = (
            "I'll help you with the payment"
        )

        # Later:
        # response = payment_service.get_payment(...)
# -----------------------------offers-------------------------------------------------------------
    elif intent == Intent.OFFER:

        response = (
            "Let me check today's offers."
        )

        # Later:
        # response = coupon_service.get_offers(...)
# ----------------------------------review-----------------------------------------------------------
    elif intent == Intent.REVIEW:

        response = (
            "I'll help you with the review."
        )

        # Later:
        # review_service.review_payment(...)
# ------------------------------------cancel order--------------------------------------------------
    elif intent == Intent.CANCEL_ORDER:

        response = (
            "Please provide your order ID."
        )

        # Later:
        # order_service.cancel_order(...)

# ------------------------------------cancel booking----------------------------------------------------

    elif intent == Intent.CANCEL_BOOKING:

        response = (
            "Please provide your booking ID to cancel the booking."
        )

        # Later:
        # booking_service.cancel_booking(...)

# --------------------track order------------------------------------------------------------------------------
    elif intent == Intent.TRACK_ORDER:

        response = (
            "Your tracking details are:"
        )
# ---------------------------------------general queries-----------------------------------------------
    else:

        response = (
            "I'm sorry, I couldn't understand your request."
        )

        # Later:
        # response = rag_service.answer(message)

# ------------------------------------------------save conversation----------------------------------
    save_conversation(

        db=db,

        customer_id=customer_id,

        user_message=message,

        bot_response=response,

        detected_intent=intent.value
    )
# ---------------------------------------------Update User History------------------------------------
    log_activity(

        db=db,

        customer_id=customer_id,

        activity=f"Chatbot detected intent: {intent.value}",

        activity_type="Chatbot"
    )
# -------------------------------------------Return Response-------------------------------------------
    return {

        "intent": intent.value,

        "response": response

    }
