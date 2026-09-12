from langgraph.graph import END, START, StateGraph

from app.ai.graph.conditional_edges import planner_edge
from app.ai.graph.state import RestaurantState


class GraphBuilder:
    """
    Responsible for building and compiling the Restaurant LangGraph workflow.

    This class ONLY defines the graph structure.
    It does not create nodes or execute the graph.
    """

    def __init__(
        self,
        load_session_node,
        planner_node,
        tool_executor_node,
        responder_node,
        save_session_node,
    ):

        self.builder = StateGraph(RestaurantState)

        self.load_session_node = load_session_node
        self.planner_node = planner_node
        self.tool_executor_node = tool_executor_node
        self.responder_node = responder_node
        self.save_session_node = save_session_node

    def add_nodes(self):
        """
        Register all graph nodes.
        """
        self.builder.add_node(
            "load_session",
            self.load_session_node
        )

        self.builder.add_node(
            "planner",
            self.planner_node
        )

        self.builder.add_node(
            "tool_executor",
            self.tool_executor_node
        )

        self.builder.add_node(
            "responder",
            self.responder_node
        )

        self.builder.add_node(
            "save_session",
            self.save_session_node
        )

    def add_edges(self):
        """
        Define graph execution flow.
        """

        self.builder.add_edge(
            START,
            "load_session"
        )

        self.builder.add_edge(
            "load_session",
            "planner"
        )

        self.builder.add_conditional_edges(
            "planner",
            planner_edge,
            {
                "tool": "tool_executor",
                "respond": "responder",
            },
        )

        self.builder.add_edge(
            "tool_executor",
            "responder"
        )

        self.builder.add_edge(
            "responder",
            "save_session"
        )

        self.builder.add_edge(
            "save_session",
            END
        )

    def build(self):
        """
        Build and compile the graph.
        """

        self.add_nodes()
        self.add_edges()

        return self.builder.compile()
