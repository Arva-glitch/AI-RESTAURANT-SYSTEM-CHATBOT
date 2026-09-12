from app.ai.graph.state import RestaurantState


def planner_router(
    state: RestaurantState,
):

    if state["selected_tool"] is None:
        return "respond"

    return "tool"
