from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.customer_favourites import CustomerFavourite


customer_favourite_crud = CRUDBase(CustomerFavourite)


def get_favourites_by_customer(
    db: Session,
    customer_id: int
):

    return (
        db.query(CustomerFavourite)
        .filter(
            CustomerFavourite.customer_id ==
            customer_id
        )
        .all()
    )


def get_favourite_menu_items(
    db: Session,
    menu_id: int
):

    return (
        db.query(CustomerFavourite)
        .filter(
            CustomerFavourite.menu_id ==
            menu_id
        )
        .all()
    )


def remove_favourite(
    db: Session,
    favourite_id: int
):

    return customer_favourite_crud.delete(
        db,
        favourite_id
    )
