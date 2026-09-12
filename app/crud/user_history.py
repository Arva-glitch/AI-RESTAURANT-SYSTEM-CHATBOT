from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_history import UserHistory


user_history_crud = CRUDBase(UserHistory)


def get_user_history(
    db: Session,
    customer_id: int
):

    return (
        db.query(UserHistory)
        .filter(
            UserHistory.customer_id ==
            customer_id
        )
        .order_by(
            UserHistory.created_at.desc()
        )
        .all()
    )


def get_recent_history(
    db: Session,
    customer_id: int,
    limit: int = 10
):

    return (
        db.query(UserHistory)
        .filter(
            UserHistory.customer_id ==
            customer_id
        )
        .order_by(
            UserHistory.created_at.desc()
        )
        .limit(limit)
        .all()
    )
