from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.review import Review


review_crud = CRUDBase(Review)


def get_review(
    db: Session,
    review_id: int
):

    return review_crud.get(db, review_id)


def get_reviews_by_customer(
    db: Session,
    customer_id: int
):

    return (
        db.query(Review)
        .filter(
            Review.customer_id == customer_id
        )
        .all()
    )


def get_reviews_by_restaurant(
    db: Session,
    restaurant_description_id: int
):

    return (
        db.query(Review)
        .filter(
            Review.restaurant_description_id ==
            restaurant_description_id
        )
        .all()
    )


def get_review_by_order(
    db: Session,
    order_id: int
):

    return (
        db.query(Review)
        .filter(
            Review.order_id == order_id
        )
        .first()
    )
