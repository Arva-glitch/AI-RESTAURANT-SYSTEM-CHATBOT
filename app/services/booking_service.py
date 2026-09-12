from datetime import date, time, datetime
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.dining_table import Diningtable
from app.crud.booking import booking_crud
from app.crud.customer import get_customer
from app.schemas.booking import BookingCreate
from app.crud.restaurantdescription import (
    get_restaurant_description
)
from app.schemas.enums import BookingStatus

from app.ai.graph.constants.booking_fields import (
    REQUIRED_BOOKING_FIELDS,
)

from app.ai.flow_manager import FlowManager

# ------------to chcek the customer----------------------------------------------------------------
print("🔥 BOOKING SERVICE FILE LOADED 🔥")


class BookingService:

    def __init__(self, db: Session):
        self.db = db

    # def process_booking():
    #      pass

    def validate_customer(

            self,
            customer_id: int
    ):
        customer = get_customer(
            self.db,
            customer_id
        )
        return customer is not None

# ------------------------------------------------------------------------------------------

    def is_restaurant_open(
            self,
            restaurant_description_id: int,
            booking_time: time
    ):
        restaurant = get_restaurant_description(
            self.db,
            restaurant_description_id
        )
        if restaurant is None:
            raise ValueError("Restaurant not found.")
        return (
            restaurant.opening_time
            <= booking_time
            <= restaurant.closing_time
        )
# -------------------------------------------------------------------------------------------

    def validate_booking_date(
            self,
            booking_date: date
    ):
        return booking_date >= date.today()

# -------------------------------------------------------------------------------------------

    def find_available_table(
        self,
        booking_date,
        booking_time,
        guests
    ):
        """
        Returns the smallest available table
        that can accommodate the guests.
        """

        tables = (
            self.db.query(Diningtable)
            .filter(
                Diningtable.seating_capacity >= guests
            )
            .order_by(Diningtable.seating_capacity)
            .all()
        )

        for table in tables:
            existing_booking = (
                self.db.query(Booking)
                .filter(
                    Booking.table_id == table.table_id,
                    Booking.booking_date == booking_date,
                    Booking.booking_time == booking_time,
                    Booking.booking_status != "Cancelled"
                )
                .first()
            )
            if existing_booking is None:
                return table
        return None

# ----------------------------------------------------------------------------------------------

    def book_table(
            self,
            booking: BookingCreate,
    ):
        if not self.validate_customer(
            booking.customer_id
        ):
            raise ValueError(
                "Customer does not exist."

            )
        if not self.validate_booking_date(
            booking.booking_date
        ):
            raise ValueError(
                "Booking date cannot be in the past."
            )

        if not self.is_restaurant_open(
            booking.restaurant_id,
            booking.booking_time
        ):
            raise ValueError(
                "Restaurant is closed at the requested time."
            )
        table = self.find_available_table(
            booking.booking_date,
            booking.booking_time,
            booking.number_of_guests
        )
        if table is None:
            raise ValueError("No tables available.")

        booking.table_id = table.table_id
        booking.booking_status = BookingStatus.confirmed

        return booking_crud.create(
            self.db,
            booking
        )

    # -------------------------------------------------------------

    def process_booking(  # it just sees whether it has enough info to create booking
            self,
            customer_id: int,
            tool_input: dict,
            context: dict,
    ) -> dict:

        booking_context = context.get("booking", {}).copy()
        print("=" * 60)
        print("BOOKING CONTEXT BEFORE UPDATE")
        print(booking_context)
        print("TOOL INPUT")
        print(tool_input)

        booking_context.update(tool_input)
        print("BOOKING CONTEXT AFTER UPDATE")
        print(booking_context)
        print("=" * 60)

        missing_fields = []
        for field in REQUIRED_BOOKING_FIELDS:
            if not booking_context.get(field):
                missing_fields.append(field)

        if missing_fields:
            context["booking"] = booking_context
            return {
                "status": "awaiting_input",

                "next_field": missing_fields[0],

                "remaining_fields": missing_fields[1:],

                "context": context
            }
        # All required information has been collected.
        print("Booking context is complete.")

        booking_date = booking_context["booking_date"]
        if not self.validate_booking_date(
            booking_date
        ):
            return {
                "status": "failed",

                "reason": "Booking date cannot be in the past.",

                "context": context,
            }

        if not self.is_restaurant_open(

            booking_context["restaurant_id"],

            booking_context["booking_time"],
        ):
            return {

                "status": "failed",

                "reason": "Restaurant is closed during the selected time.",

                "context": context,
            }
        table = self.find_available_table(
            booking_date=booking_context["booking_date"],
            booking_time=booking_context["booking_time"],
            guests=booking_context["number_of_guests"],
        )
        if table is None:
            return {
                "status": "booking_unavailable",
                "context": context,
            }

        booking = BookingCreate(
            customer_id=customer_id,

            restaurant_id=booking_context["restaurant_id"],

            booking_date=booking_context["booking_date"],

            booking_time=booking_context["booking_time"],

            number_of_guests=booking_context["number_of_guests"],

            special_request=booking_context.get(
                "special_request"
            ),

            occasion=booking_context.get(
                "occasion"
            ),

            booking_source="Telegram",
        )

        booking_result = self.book_table(
            booking)

        FlowManager.clear_flow(context)
        context["booking"] = {}

        return {

            "status": "booking_confirmed",

            "booking": booking_result,

            "context": context,
        }
