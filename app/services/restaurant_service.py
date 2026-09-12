from sqlalchemy.orm import Session
from app.crud.restaurantdescription import get_restaurant_description


class RestaurantService:

    def __init__(self, db: Session):
        self.db = db

    def get_restaurant_information(
            self,
            restaurant_id: int,) -> dict | None:
        """
        Returns the restaurant's basic information.
        """

        restaurant = get_restaurant_description(
            self.db,
            restaurant_id
        )

        if restaurant is None:
            return None

        # Call CRUD here

        return {
            "restaurant_id": restaurant.restaurant_id,
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_address": restaurant.restaurant_address,
            "restaurant_landmark": restaurant.restaurant_landmark,
            "phone_number": restaurant.phone_number,
            "email": restaurant.email,
            "opening_time": str(restaurant.opening_time),
            "closing_time": str(restaurant.closing_time),
            "cuisine_type": restaurant.cuisine_type,
            "restaurant_status": restaurant.restaurant_status,
            "average_cost_for_two": restaurant.average_cost_for_two,
        }
