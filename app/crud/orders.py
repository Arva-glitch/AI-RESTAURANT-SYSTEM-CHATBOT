from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.orders import Order


order_crud = CRUDBase(Order)


def get_orders_by_customer(
    db: Session,
    customer_id: int
):

    return (
        db.query(Order)
        .filter(
            Order.customer_id == customer_id
        )
        .all()
    )


def get_orders_by_booking(
    db: Session,
    booking_id: int
):

    return (
        db.query(Order)
        .filter(
            Order.booking_id == booking_id
        )
        .all()
    )


def update_order_status(
    db: Session,
    order_id: int,
    status: str
):

    order = order_crud.get(
        db,
        order_id
    )

    if order:

        order.order_status = status

        db.commit()

        db.refresh(order)

    return order
