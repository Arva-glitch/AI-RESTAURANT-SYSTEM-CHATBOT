# from app.ai.graph.state import RestaurantState

# from app.services.booking_service import BookingService
# from app.tools.base_tool import BaseTool
# from app.ai.graph.state import RestaurantState
# from app.ai.flow_manager import FlowManager


# class BookingTool(BaseTool):

#     name = "booking"

#     description = (
#         "Book tables, check availability, "
#         "modify bookings and cancel bookings."
#     )

#     def __init__(
#         self,
#         state: RestaurantState,
#     ) -> RestaurantState:
#         self.booking_service = booking_service

#     def execute(
#         self,
#         tool_input: dict,
#     ) -> dict:
#         """
#         Placeholder.
#         We'll integrate booking_service next.
#         """

#         return self.booking_service.process_booking(
#             tool_input
#         )

from app.ai.flow_manager import FlowManager
from app.ai.graph.state import RestaurantState

from app.services.booking_service import BookingService
from app.tools.base_tool import BaseTool

from app.ai.flow_type import FlowType


class BookingTool(BaseTool):

    name = "booking"

    description = (
        "Book tables, check availability, "
        "modify bookings and cancel bookings."
    )

    def __init__(
        self,
        booking_service: BookingService,
    ):
        self.booking_service = booking_service

    def execute(
        self,
        state: RestaurantState,
    ) -> RestaurantState:

        print("🔥 BOOKING TOOL EXECUTE 🔥")

        # Set active conversation flow
        if FlowManager.get_flow(state["context"]) is None:
            FlowManager.set_flow(
                state["context"],
                FlowType.BOOKING
            )
        try:
            result = self.booking_service.process_booking(
                customer_id=state["customer_id"],
                tool_input=state["tool_input"],
                context=state["context"],
            )
        except Exception as e:
            raise RuntimeError(
                f"BookingTool failed: {e}"
            ) from e

        print("=" * 60)
        print("BOOKING TOOL RESULT")
        print(result)
        print("=" * 60)

        state["tool_output"] = result

        if "context" in result:
            state["context"] = result["context"]

            return state
