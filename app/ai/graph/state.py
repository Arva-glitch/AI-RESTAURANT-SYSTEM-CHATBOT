from typing import Annotated, Any
from app.models.chatbot_session import ChatBotSession
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class RestaurantState(TypedDict):
    """
    Shared state across the entire LangGraph workflow.
    """

    # LangGraph conversation history
    messages: Annotated[list[BaseMessage], add_messages]

    # Current user input
    user_message: str

    # Current AI response
    response: str

    # Database identifiers
    customer_id: int
    session_id: int

    # Complete session context from ChatBotSession.context
    context: dict[str, Any]

    # Intent
    intent: str | None

    # Current reasoning
    goal: str | None

    # Tool to execute
    selected_tool: str | None

    # Parameters extracted for the tool
    tool_input: dict[str, Any]

    # Result returned by the tool
    tool_output: dict[str, Any] | None

    # Extra information
    metadata: dict[str, Any]

    # restaurant state
    session: ChatBotSession
