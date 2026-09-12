from sqlalchemy.orm import Session

from app.crud.user_history import (
    user_history_crud,
    get_user_history,
    get_recent_history
)

from app.schemas.user_history import (
    UserHistoryCreate
)

from app.models.user_history import UserHistory

from app.schemas.enums import ActivityType

# --------------------------------------------------------------------------------------------------


def log_activity(
    db: Session,
    customer_id: int,
    activity: str,
    activity_type: str
):

    history = UserHistoryCreate(
        customer_id=customer_id,
        activity=activity,
        activity_type=activity_type
    )

    return user_history_crud.create(
        db,
        history
    )
# --------------------------------------------------------------------------------------------------


def fetch_user_history(
    db: Session,
    customer_id: int
):

    return get_user_history(
        db,
        customer_id
    )
# -----------------------------------------------------------------------------------------------------


def fetch_recent_history(
    db: Session,
    customer_id: int,
    limit: int = 10
):

    return get_recent_history(
        db,
        customer_id,
        limit
    )
# --------------------------------------------------------------------------------------------------


def get_history_by_type(
    db: Session,
    customer_id: int,
    activity_type: ActivityType
):

    return (
        db.query(UserHistory)
        .filter(
            UserHistory.customer_id == customer_id,
            UserHistory.activity_type == activity_type
        )
        .order_by(UserHistory.created_at.desc())
        .all()
    )
# ------------------------------------------------------------------------------------------------------
