from app.ai.graph.state import RestaurantState


def planner_edge(state: RestaurantState):

    if state["selected_tool"]:
        return "tool"

    return "respond"
