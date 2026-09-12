from app.ai.flow_type import FlowType


class FlowManager:
    """
    Responsible for managing the active conversation flow.
    """

    @staticmethod
    def set_flow(
        context: dict,
        flow: FlowType,
    ) -> None:

        context["active_flow"] = flow.value

    @staticmethod
    def get_flow(
        context: dict,
    ) -> str | None:

        return context.get("active_flow")

    @staticmethod
    def clear_flow(
        context: dict,
    ) -> None:

        context["active_flow"] = None
