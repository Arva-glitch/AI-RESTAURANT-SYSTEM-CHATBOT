# here we want a structured output rather than a normal string stating what to do

from pydantic import BaseModel, Field
from typing import Any


class PlannerOutput(BaseModel):
    """
    Structured response returned by the planner LLM.
    """

    intent: str = Field(
        description="Detected user intent."
    )

    goal: str = Field(
        description="Overall goal of the user."
    )

    selected_tool: str | None = Field(
        default=None,
        description="Tool to execute."
    )

    tool_input: dict[str, Any] = Field(
        default_factory=dict,
        description="Arguments for the selected tool."
    )

    reasoning: str = Field(
        description="Why this tool was selected."
    )
