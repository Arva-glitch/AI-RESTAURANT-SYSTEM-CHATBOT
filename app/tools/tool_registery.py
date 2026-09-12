# This registry is what the PlannerNode will inspect.
# its job is simple:
# Register all available tools.
# Return a tool when given its name.

from app.tools.base_tool import BaseTool


class ToolRegistry:

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        if tool.name in self._tools:
            raise ValueError(
                f"Tool '{tool.name}' is already registered."
            )
        self._tools[tool.name] = tool

    def get(self, tool_name: str) -> BaseTool | None:
        return self._tools.get(tool_name)

    def list_tools(self) -> list[BaseTool]:
        return list(self._tools.values())

    def get_tool_descriptions(self) -> str:
        """
        Returns formatted tool descriptions for the planner prompt.
        """

        return "\n".join(
            [
                f"- {tool.name}: {tool.description}"
                for tool in self._tools.values()
            ]
        )
