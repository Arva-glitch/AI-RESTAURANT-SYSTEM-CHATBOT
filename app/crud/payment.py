from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.payment import Payment


payment_crud = CRUDBase(Payment)


def get_payment_by_bill(
    db: Session,
    bill_id: int
):

    return (
        db.query(Payment)
        .filter(
            Payment.bill_id == bill_id
        )
        .first()
    )


def update_payment_status(
    db: Session,
    payment_id: int,
    status: str
):

    payment = payment_crud.get(
        db,
        payment_id
    )

    if payment:

        payment.payment_status = status

        db.commit()

        db.refresh(payment)

    return payment
