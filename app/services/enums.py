# ismai I have enums for my services

from enum import Enum


class ActivityType(str, Enum):  # this is the enum for activity type in user_history_services.py
    BOOKING = "Booking"
    ORDER = "Order"
    PAYMENT = "Payment"
    CHATBOT = "Chatbot"
    REVIEW = "Review"
    COUPON = "Coupon"
