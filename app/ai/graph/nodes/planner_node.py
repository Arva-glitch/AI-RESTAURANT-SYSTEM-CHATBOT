# This is the AI brain.


from app.ai.graph.state import RestaurantState
from app.ai.graph.prompts.planner_prompt import build_planner_prompt
from app.ai.graph.schemas.planner_output import PlannerOutput
from langchain_core.language_models import BaseChatModel
from app.tools.tool_registery import ToolRegistry


class PlannerNode:

    def __init__(self, llm: BaseChatModel, registry: ToolRegistry):
        self.llm = llm
        self.registry = registry

    def __call__(
        self,
        state: RestaurantState,
    ) -> RestaurantState:

        # Read the information we need
        context = state.get("context", {})
        user_message = state["user_message"]

        tool_descriptions = self.registry.get_tool_descriptions()

        prompt = build_planner_prompt(
            tool_descriptions=tool_descriptions,
            context=context,
            user_message=user_message,
        )

        structured_llm = self.llm.with_structured_output(
            PlannerOutput
        )

        try:
            planner_result = structured_llm.invoke(prompt)
        except Exception as e:
            raise RuntimeError(
                f"PlannerNode failed: {e}"
            ) from e

        state["intent"] = planner_result.intent

        state["goal"] = planner_result.goal
        state["selected_tool"] = planner_result.selected_tool
        state["tool_input"] = planner_result.tool_input
        state["metadata"]["planner_reasoning"] = planner_result.reasoning

        return state
