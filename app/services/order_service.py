from app.schemas.place_order import (
    PlaceOrderRequest,
    PlaceOrderResponse
)
from typing import List
from app.schemas.place_order import OrderItemRequest
from sqlalchemy.orm import Session
from decimal import Decimal
from app.crud.orders import order_crud
from app.crud.order_items import order_item_crud
from app.crud.customer import get_customer
from app.models.menu import Menu
from app.models.inventory import Inventory
from app.schemas.orders import OrderCreate
from app.schemas.order_items import OrderItemCreate
from app.services.customer_service import validate_customer
from app.services.inventory_service import consume_inventory
# ---------------------------------------------------------------------------------------


def validate_menu_item(
    db: Session,
    menu_id: int
):

    menu = (
        db.query(Menu)
        .filter(Menu.menu_id == menu_id)
        .first()
    )

    if menu is None:
        raise ValueError("Menu item not found.")

    if not menu.is_available:
        raise ValueError(f"{menu.food_name} is currently unavailable.")

    return menu
# -----------------------------------------------------------------------------------------


def check_inventory(
    db: Session,
    menu_id: int,
    quantity: int
):

    inventory = (
        db.query(Inventory)
        .filter(Inventory.menu_id == menu_id)
        .first()
    )

    if inventory is None:
        raise ValueError("Inventory not found.")

    if inventory.quantity_available < quantity:
        raise ValueError("Insufficient stock.")

    return inventory

# ---------------------------------------------------------------------------------------


def calculate_item_total(
    price: Decimal,
    quantity: int
):

    return price * quantity
# ----------------------------------------------------------------------------------------


def calculate_subtotal(
        db: Session,
        items: List[OrderItemRequest]):

    subtotal = Decimal("0.00")

    order_items = []

    for item in items:

        menu = validate_menu_item(
            db,
            item.menu_id
        )

        inventory = check_inventory(
            db,
            item.menu_id,
            item.quantity
        )

        total = calculate_item_total(
            menu.price,
            item.quantity
        )

        subtotal += total

        order_items.append(
            {
                "menu": menu,
                "quantity": item.quantity,
                "unit_price": menu.price,
                "total_price": total
            }
        )

    return subtotal, order_items
# -----------------------------------------------------------------------------------------

# NOW WE'LL CREATE MAIN FUNCTION THAT MY CHATBOT WILL ACCESS KNOWN AS PLACE_ORDER()
# creating function skeleton


def place_order(
        db: Session,
        order_request: PlaceOrderRequest):

    customer_exists = validate_customer(
        db,
        order_request.customer_id)

    if not customer_exists:
        raise ValueError("Customer does not exist.")

    subtotal, prepared_items = calculate_subtotal(db, order_request.items)
    discount = Decimal("0.00")
    GST = Decimal("0.05")
    tax = subtotal * GST
    grand_total = subtotal + tax - discount
    order = order_crud.create(
        db,
        OrderCreate(
            customer_id=order_request.customer_id,
            booking_id=order_request.booking_id,
            restaurant_description_id=order_request.restaurant_description_id,
            coupon_id=order_request.coupon_id,
            order_type=order_request.order_type,
            order_status="Pending",
            total_amount=grand_total,
            special_instruction=order_request.special_instruction))

    for item in prepared_items:
        order_item_crud.create(
            db,
            OrderItemCreate(
                order_id=order.order_id,
                menu_id=item["menu"].menu_id,
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total_price=item["total_price"],
                item_status="Pending"
            )
        )
        inventory = check_inventory(
            db,
            item.menu_id,
            item.quantity
        )
        # inventory.quantity_available -= check_inventory(db,menu_id: int,quantity: int):
        # # generate_bill(...)
    for item in order_request.items:
        consume_inventory(db, item.menu_id, item.quantity)

    return PlaceOrderResponse(
        order_id=order.order_id,
        total_items=len(prepared_items),
        subtotal=subtotal,
        tax=tax,
        discount=discount,
        grand_total=grand_total,
        payment_status="Pending",
        message="Order placed successfully."
    )
