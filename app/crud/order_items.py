from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order_item import OrderItem


order_item_crud = CRUDBase(OrderItem)


def get_items_by_order(
    db: Session,
    order_id: int
):

    return (
        db.query(OrderItem)
        .filter(
            OrderItem.order_id == order_id
        )
        .all()
    )


def get_menu_item_count(
    db: Session,
    menu_id: int
):

    return (
        db.query(OrderItem)
        .filter(
            OrderItem.menu_id == menu_id
        )
        .count()
    )
