from app.tools.base_tool import BaseTool
from app.services.restaurant_service import RestaurantService
from app.ai.graph.state import RestaurantState


class RestaurantInfoTool(BaseTool):

    name = "restaurant_info"

    description = "Provides general information about the restaurant including " \
        "name, description, timings and location."

    def __init__(self, restaurant_service: RestaurantService,):
        self.restaurant_service = restaurant_service

    def execute(self, state: RestaurantState,) -> RestaurantState:
        tool_input = state["tool_input"]
        restaurant_id = tool_input.get(
            "restaurant_id",
            1,
        )
        result = self.restaurant_service.get_restaurant_information(
            restaurant_id
        )
        state["tool_output"] = result
        return state
