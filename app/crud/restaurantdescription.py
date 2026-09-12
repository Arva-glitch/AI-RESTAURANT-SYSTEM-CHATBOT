from sqlalchemy.orm import Session

from app.models.restaurant_description import Restaurant_Description
from app.schemas.restaurantdescription import (
    RestaurantDescriptionCreate,
    RestaurantDescriptionUpdate
)


def create_restaurant(
        db: Session,
        restaurant: RestaurantDescriptionCreate
):

    db_restaurant = Restaurant_Description(
        **restaurant.model_dump()
    )

    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def get_restaurant(
        db: Session,
        restaurant_id: int
):

    return (
        db.query(Restaurant_Description)
        .filter(
            Restaurant_Description.restaurant_id ==
            restaurant_id
        )
        .first()
    )


def update_restaurant(
        db: Session,
        restaurant_id: int,
        restaurant: RestaurantDescriptionUpdate
):

    db_restaurant = get_restaurant(
        db,
        restaurant_id
    )

    if not db_restaurant:
        return None

    update_data = restaurant.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_restaurant, key, value)

    db.commit()
    db.refresh(db_restaurant)

    return db_restaurant


def delete_restaurant(
        db: Session,
        restaurant_id: int
):

    db_restaurant = get_restaurant(
        db,
        restaurant_id
    )

    if not db_restaurant:
        return None

    db.delete(db_restaurant)
    db.commit()

    return db_restaurant


def get_restaurant_description(
    db: Session,
    restaurant_id: int
):

    return (
        db.query(Restaurant_Description)
        .filter(
            Restaurant_Description.restaurant_id == restaurant_id
        )
        .first()
    )
