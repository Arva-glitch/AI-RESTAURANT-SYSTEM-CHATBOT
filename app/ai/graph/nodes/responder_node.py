
from langchain_core.language_models import BaseChatModel
from app.ai.graph.state import RestaurantState
from app.ai.graph.prompts.responder_prompt import build_responder_prompt
from langchain_core.messages import HumanMessage, AIMessage


class ResponderNode:
    """
    Converts tool output into a natural language response.
    """

    def __init__(
        self,
        llm: BaseChatModel,
    ):
        self.llm = llm

    def _save_messages(
        self,
        state: RestaurantState,
        user_message: str,
    ) -> None:
        """
        Save conversation history into LangGraph state.
        """

        state["messages"].append(
            HumanMessage(content=user_message)
        )

        state["messages"].append(
            AIMessage(content=state["response"])
        )

    def __call__(self, state: RestaurantState
                 ) -> RestaurantState:

        user_message = state["user_message"]
        context = state.get("context", {})
        goal = state["goal"]
        tool_output = state["tool_output"]

        status = None
        if tool_output:
            status = tool_output.get("status")

        # -------------------------------------------------------
        # Booking needs more information
        # -------------------------------------------------------

        if status == "awaiting_input":
            next_field = tool_output["next_field"]

            questions = {
                "booking_date":
                "Sure! What date would you like to book the table for?",

                "booking_time":
                "Great! What time would you prefer?",

                "number_of_guests":
                "How many guests will be joining?",

                "special_request":
                "Do you have any special requests? (Optional)"
            }
            state["response"] = questions.get(
                next_field,
                "Could you provide more information?"
            )
            self._save_messages(
                state,
                user_message
            )

            return state

        # -------------------------------------------------------
        # Booking successful
        # -------------------------------------------------------

        if status == "booking_confirmed":
            booking = tool_output["booking"]
            state["response"] = (
                f"🎉 Your table has been booked successfully!"
            )
            self._save_messages(
                state,
                user_message
            )

            return state

        # -------------------------------------------------------
        # No table available
        # -------------------------------------------------------

        if status == "booking_unavailable":

            state["response"] = (
                "Sorry, there are no tables available "
                "for the selected time."
            )

            self._save_messages(
                state,
                user_message
            )

            return state

        # -------------------------------------------------------
        # booking failure
        # ------------------------------------------------------
        if status == "failed":
            state["response"] = tool_output["reason"]
            self._save_messages(
                state,
                user_message
            )
            return state

        # -------------------------------------------------------
        # LLM Response
        # -------------------------------------------------------

        prompt = build_responder_prompt(
            user_message=user_message,
            context=context,
            goal=goal,
            tool_output=tool_output,
        )

        try:
            print("=" * 50)
            print("TOOL OUTPUT")
            print(tool_output)
            print("=" * 50)
            response = self.llm.invoke(prompt)
        except Exception as e:
            raise RuntimeError(
                f"ResponderNode failed: {e}"
            ) from e

        state["response"] = response.content
        self._save_messages(
            state,
            user_message
        )
        return state
