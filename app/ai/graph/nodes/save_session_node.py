# this is the personality of our chatbot

from app.ai.graph.state import RestaurantState
from app.chatbot.session_manager import SessionManager


class SaveSessionNode:

    def __init__(self, session_manager):
        self.session_manager = session_manager

    def __call__(
        self,
        state: RestaurantState,
    ) -> RestaurantState:

        print("=" * 60)
        print("CONTEXT BEFORE SAVE")
        print(state["context"])
        print("=" * 60)

        self.session_manager.save_context(
            session=state["session"],
            context=state["context"],
        )

        return state
