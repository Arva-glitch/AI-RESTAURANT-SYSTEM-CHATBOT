# here this for my chatbot_service.py


from enum import Enum


class Intent(str, Enum):

    BOOK_TABLE = "book_table"
    ORDER_ONLINE = "order_online"
    VIEW_MENU = "view_menu"
    APPLY_COUPON = "apply_coupon"
    PAYMENT = "payment"
    TRACK_ORDER = "track_order"
    CANCEL_BOOKING = "cancel_booking"
    CANCEL_ORDER = "cancel_order"
    REVIEW = "review"
    FAQ = "faq"
    UNKNOWN = "unknown"
# ----------------------------------------------------------------


INTENT_KEYWORDS = {

    Intent.BOOK_TABLE: [
        "book",
        "booking",
        "reserve",
        "reservation",
        "table"
    ],

    Intent.ORDER_ONLINE: [
        "order",
        "food",
        "eat",
        "hungry",
        "delivery",
        "deliver"
    ],

    Intent.VIEW_MENU: [
        "menu",
        "dish",
        "food items"
    ],

    Intent.APPLY_COUPON: [
        "coupon",
        "offer",
        "discount",
        "promo"
    ],

    Intent.PAYMENT: [
        "pay",
        "payment",
        "bill"
    ],

    Intent.REVIEW: [
        "review",
        "rating",
        "feedback"
    ],

    Intent.CANCEL_BOOKING: [
        "cancel booking",
        "cancel reservation"
    ],

    Intent.CANCEL_ORDER: [
        "cancel order"
    ],

    Intent.TRACK_ORDER: [
        "track order",
        "where is my order",
        "status"
    ]
}


def detect_intent(message: str) -> Intent:

    message = message.lower()

    for intent, keywords in INTENT_KEYWORDS.items():

        if any(keyword in message for keyword in keywords):

            return intent

        return Intent.UNKNOWN
# -----------------------------------------------------------------
    # if any(word in message for word in cancel_booking_keywords):
    #     return Intent.CANCEL_BOOKING

    # if any(word in message for word in cancel_order_keywords):
    #     return Intent.CANCEL_ORDER

    # if any(word in message for word in booking_keywords):
    #     return Intent.BOOKING

    # if any(word in message for word in order_keywords):
    #     return Intent.ORDER

    # if any(word in message for word in menu_keywords):
    #     return Intent.MENU

    # if any(word in message for word in offer_keywords):
    #     return Intent.OFFER

    # if any(word in message for word in payment_keywords):
    #     return Intent.PAYMENT

    # if any(word in message for word in review_keywords):
    #     return Intent.REVIEW

    # return Intent.GENERAL
