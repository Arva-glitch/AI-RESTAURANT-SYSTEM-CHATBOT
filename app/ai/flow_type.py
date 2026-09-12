from enum import Enum


class FlowType(str, Enum):

    BOOKING = "booking"

    ORDER = "order"

    REVIEW = "review"

    PAYMENT = "payment"

    GENERAL = "general"
