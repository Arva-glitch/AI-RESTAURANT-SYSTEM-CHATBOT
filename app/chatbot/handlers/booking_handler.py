from datetime import datetime

from sqlalchemy.orm import Session

from app.chatbot.handlers.base_handler import BaseHandler

from app.chatbot.states import ChatState


from app.schemas.booking import BookingCreate

from app.services.booking_service import book_table

from app.chatbot.prompts import MAIN_MENU

# ---------------------------------------------------------------------------------------


class BookingHandler(BaseHandler):

    def __init__(self, db: Session):
        super().__init__(db)

    def handle(
        self,
        customer,
        session,
        message: str
    ) -> str:

        if session.current_state == ChatState.BOOKING_DATE.value:
            return self.handle_booking_date(
                session,
                message
            )

        elif session.current_state == ChatState.BOOKING_TIME.value:
            return self.handle_booking_time(
                session,
                message
            )

        elif session.current_state == ChatState.BOOKING_GUESTS.value:
            return self.handle_booking_guests(
                customer,
                session,
                message
            )

        elif session.current_state == ChatState.BOOKING_CONFIRMATION.value:
            return self.handle_booking_confirmation(
                customer,
                session,
                message
            )

        return "Invalid booking state."
# -----------------------------------------------------------

    def handle_booking_date(
        self,
        session,
        message: str
    ):
        try:
            booking_date = datetime.strptime(
                message,
                "%d-%m-%Y"
            ).date()

        except ValueError:
            return (
                "❌ Invalid date format.\n\n"
                "Please enter the date as DD-MM-YYYY.\n"
                "Example: 25-07-2026"
            )

        if booking_date < datetime.today().date():
            return (
                "❌ Booking date cannot be in the past.\n\n"
                "Please enter a future date."
            )
        context = dict(self.session_manager.get_context(session))
        booking = dict(context.get("booking", {}))

        booking["date"] = booking_date.isoformat()

        context["booking"] = booking
        self.session_manager.save_context(
            session,
            context
        )

        self.session_manager.set_state(
            session,
            ChatState.BOOKING_TIME.value
        )

        print("AFTER DATE SAVE")
        print(self.session_manager.get_context(session))
        return (
            "✅ Date saved successfully!\n\n"
            "⏰ Please enter your booking time.\n"
            "Example: 07:30 PM"
        )
# ----------------------------------------------------------------

    def handle_booking_time(
        self,
        session,
        message: str
    ):

        try:
            booking_time = datetime.strptime(
                message,
                "%I:%M %p"
            ).time()

        except ValueError:
            return (
                "❌ Invalid time format.\n\n"
                "Example:\n"
                "07:30 PM"
            )

        context = dict(self.session_manager.get_context(session))

        booking = dict(context.get("booking", {}))

        booking["time"] = booking_time.strftime("%H:%M")

        context["booking"] = booking
        self.session_manager.save_context(
            session,
            context
        )
        self.session_manager.set_state(
            session,
            ChatState.BOOKING_GUESTS.value
        )

        # print("After TIME save:")
        # print(self.session_manager.get_context(session))

        return (
            "👥 Please enter the number of guests.\n\n"
            "Example:\n"
            "4"
        )
# --------------------------------------------------------------------

    def handle_booking_guests(
        self,
        customer,
        session,
        message: str
    ):
        try:
            guests = int(message)

        except ValueError:

            return (
                "❌ Please enter a valid number of guests."
            )

        MAX_GUESTS = 20
        if guests < 1 or guests > MAX_GUESTS:
            return (
                f"❌ Please enter a valid number of guests (1-{MAX_GUESTS})."
            )

        print("Before GUESTS:")
        print(self.session_manager.get_context(session))

        context = dict(self.session_manager.get_context(session))

        booking = dict(context.get("booking", {}))

        booking["guests"] = guests
        context["booking"] = booking

        self.session_manager.save_context(
            session,
            context
        )
        self.session_manager.set_state(
            session,
            ChatState.BOOKING_CONFIRMATION.value
        )

        print(context)
        print(booking)

        print("=" * 50)
        print("FULL CONTEXT:", context)
        print("BOOKING:", booking)
        print("=" * 50)

        return (
            "📋 Booking Summary\n\n"
            f"📅 Date : {booking.get('date')}\n"
            f"⏰ Time : {booking.get('time')}\n"
            f"👥 Guests : {booking.get('guests')}\n\n"
            "Reply YES to confirm.\n"
            "Reply NO to cancel."
        )
# ----------------------------------------------------------------------------------------

    def handle_booking_confirmation(
        self,
        customer,
        session,
        message: str
    ):
        message = message.strip().upper()
        if message == "NO":
            self.session_manager.clear_context(session)

            self.session_manager.set_state(
                session,
                ChatState.MAIN_MENU.value
            )
            return (
                "❌ Booking cancelled.\n\n"
                f"{MAIN_MENU}"
            )
        if message != "YES":
            return "❓ Please reply with YES or NO."

        context = self.session_manager.get_context(session)
        booking = context.get("booking", {})
        required_fields = ["date", "time", "guests"]

        missing = [
            field for field in required_fields
            if field not in booking
        ]

        if missing:
            return (
                "❌ Booking information is incomplete.\n"
                "Please start the booking process again."
            )

        try:

            booking_data = BookingCreate(
                customer_id=customer.customer_id,
                restaurant_id=1,
                booking_date=datetime.strptime(
                    booking["date"],
                    "%Y-%m-%d"
                ).date(),
                booking_time=datetime.strptime(
                    booking["time"],
                    "%H:%M"
                ).time(),
                number_of_guests=booking["guests"],
                special_request=None
            )
            created_booking = book_table(
                self.db,
                booking_data
            )

        except Exception as e:
            return f"❌ Booking failed.\n\n{str(e)}"
        self.session_manager.clear_context(session)
        self.session_manager.set_state(
            session,
            ChatState.MAIN_MENU.value
        )
        return (
            "🎉 Booking Confirmed!\n\n"
            f"🆔 Booking ID: {created_booking.booking_id}\n"
            f"📅 Date: {booking['date']}\n"
            f"⏰ Time: {booking['time']}\n"
            f"👥 Guests: {booking['guests']}\n\n"
            f"{MAIN_MENU}"
        )
