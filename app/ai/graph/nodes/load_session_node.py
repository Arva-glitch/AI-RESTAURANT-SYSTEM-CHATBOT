# Its only job is:Load customer's session

from app.ai.graph.state import RestaurantState
from app.chatbot.session_manager import SessionManager


class LoadSessionNode:
    """
    Loads the current chatbot session into the graph state.
    """

    def __init__(self,
                 session_manager: SessionManager,
                 ):
        self.session_manager = session_manager

    def __call__(self, state: RestaurantState) -> RestaurantState:

        session = self.session_manager.get_or_create(
            customer_id=state["customer_id"]
        )

        state["session"] = session
        state["session_id"] = session.session_id   # optional
        # state["context"] = self.session_manager.get_context(session)

        context = self.session_manager.get_context(session)
        print("=" * 60)
        print("CONTEXT AFTER LOAD")
        print(state["context"])
        print("=" * 60)

        state["context"] = context

        return state
