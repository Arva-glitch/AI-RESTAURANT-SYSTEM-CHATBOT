from enum import Enum


class BookingStatus(str, Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    cancelled = "Cancelled"
    completed = "Completed"


class OrderStatus(str, Enum):
    pending = "Pending"
    confirmed = "Confirmed"
    preparing = "Preparing"
    ready = "Ready"
    delivered = "Delivered"
    completed = "Completed"
    cancelled = "Cancelled"


class ItemStatus(str, Enum):
    pending = "Pending"
    preparing = "Preparing"
    ready = "Ready"
    served = "Served"
    cancelled = "Cancelled"


class PaymentStatus(str, Enum):
    pending = "Pending"
    successful = "Successful"
    failed = "Failed"
    refunded = "Refunded"


class OrderType(str, Enum):
    dine_in = "Dine In"
    takeaway = "Takeaway"
    delivery = "Delivery"


class TableStatus(str, Enum):
    available = "Available"
    occupied = "Occupied"
    reserved = "Reserved"


class PaymentMethod(str, Enum):
    cash = "Cash"
    upi = "UPI"
    debit_card = "Debit Card"
    credit_card = "Credit Card"
    net_banking = "Net Banking"
