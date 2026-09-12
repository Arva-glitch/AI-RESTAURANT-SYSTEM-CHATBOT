from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bill import Bill


bill_crud = CRUDBase(Bill)


def get_bill_by_order(
    db: Session,
    order_id: int
):

    return (
        db.query(Bill)
        .filter(
            Bill.order_id == order_id
        )
        .first()
    )
