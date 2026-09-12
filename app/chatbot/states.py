from enum import Enum


class ChatState(str, Enum):

    # Initial States
    START = "START"
    WELCOME = "WELCOME"
    REGISTER = "REGISTER"
    MAIN_MENU = "MAIN_MENU"

    # Booking Flow
    BOOKING_DATE = "BOOKING_DATE"
    BOOKING_TIME = "BOOKING_TIME"
    BOOKING_GUESTS = "BOOKING_GUESTS"
    BOOKING_CONFIRMATION = "BOOKING_CONFIRMATION"

    # Online Ordering Flow
    ORDER_TYPE = "ORDER_TYPE"
    DELIVERY_ADDRESS = "DELIVERY_ADDRESS"

    # Menu & Order
    MENU = "MENU"
    ORDERING = "ORDERING"
    CART = "CART"

    # Payment
    APPLY_COUPON = "APPLY_COUPON"
    PAYMENT = "PAYMENT"

    # Feedback
    REVIEW = "REVIEW"

    # End
    COMPLETED = "COMPLETED"
