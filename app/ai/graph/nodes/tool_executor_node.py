
from app.ai.graph.state import RestaurantState
from app.tools.tool_registery import ToolRegistry


class ToolExecutorNode:
    """
    Executes the tool selected by the planner.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ):
        self.registry = registry

    def __call__(
        self,
        state: RestaurantState,
    ) -> RestaurantState:

        tool_name = state["selected_tool"]
        if not tool_name:
            raise ValueError(
                "Planner did not select a tool."
            )

        tool = self.registry.get(tool_name)

        if tool is None:
            raise ValueError(
                f"Tool '{tool_name}' is not registered."
            )

        try:
            print("=" * 60)
            print("Selected Tool:", tool_name)
            print("State before execute:", state)
            print("=" * 60)
            state = tool.execute(state)
            print("=" * 60)
            print("State after execute:", state)
            print("=" * 60)
            # state = tool.execute(state)

        except Exception as e:
            raise RuntimeError(
                f"Execution of '{tool_name}' failed: {e}"
            ) from e

        state["metadata"]["executed_tool"] = tool_name

        return state
