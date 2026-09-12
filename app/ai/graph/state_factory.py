from app.ai.graph.state import RestaurantState
from langchain_core.messages import HumanMessage


class StateFactory:
    """
    Responsible for creating the initial RestaurantState
    before the graph execution begins.
    """

    @staticmethod
    def create(
        customer_id: int,
        user_message: str,
    ) -> RestaurantState:
        return {

            "session": None,

            "customer_id": customer_id,

            "session_id": None,

            "user_message": user_message,

            "messages": [HumanMessage(content=user_message)],

            "context": {
                "active_flow": None,
                "booking": {
                    "booking_date": None,

                    "booking_time": None,

                    "number_of_guests": None,

                    "special_request": None,

                    "restaurant_id": 1
                },

                "order": {
                    "fulfillment_type": None,

                    "cart": [],

                    "delivery_address": None,

                    "coupon": None,

                    "payment_status": None,

                    "order_status": None
                },
                "customer": {"customer_id": customer_id
                             }

            },

            "goal": None,

            "selected_tool": None,

            "tool_input": {},

            "tool_output": None,

            "response": "",

            "metadata": {},
        }
