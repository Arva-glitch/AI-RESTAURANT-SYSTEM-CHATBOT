# restaurantgraphservice will create dependencies only
# and grph builder will create nodes, connect nodes,compiles graph
# here this restaurantgraphservice manages AI conversations
# RestaurantGraphService has only three responsibilities:
# '''
# 1. Initialize dependencies

# 2. Build the graph

# 3. Execute the graph
# '''

# This is the bridge between your application and LangGraph.


from sqlalchemy.orm import Session

from app.ai.graph.builder import GraphBuilder
from app.ai.graph.state_factory import StateFactory
from app.chatbot.session_manager import SessionManager

from app.tools.tool_registery import ToolRegistry
from app.ai.llm.groq_client import llm

from app.ai.graph.nodes.load_session_node import LoadSessionNode
from app.ai.graph.nodes.planner_node import PlannerNode
from app.ai.graph.nodes.tool_executor_node import ToolExecutorNode
from app.ai.graph.nodes.responder_node import ResponderNode
from app.ai.graph.nodes.save_session_node import SaveSessionNode
from app.tools.restaurant_info_tool import RestaurantInfoTool
from app.services.restaurant_service import RestaurantService
from app.services.booking_service import BookingService
from app.tools.booking_tool import BookingTool


class RestaurantGraphService:

    def __init__(self, db: Session):
        self.db = db

        # shared dependencies
        self.session_manager = SessionManager(db)
        self.llm = llm
        self.registry = ToolRegistry()

        # Nodes

        self.load_session_node = LoadSessionNode(
            session_manager=self.session_manager
        )

        self.planner_node = PlannerNode(
            llm=self.llm,
            registry=self.registry
        )

        self.tool_executor_node = ToolExecutorNode(
            registry=self.registry
        )

        self.responder_node = ResponderNode(
            llm=self.llm
        )

        self.save_session_node = SaveSessionNode(
            session_manager=self.session_manager
        )

        self.graph_builder = GraphBuilder(
            load_session_node=self.load_session_node,
            planner_node=self.planner_node,
            tool_executor_node=self.tool_executor_node,
            responder_node=self.responder_node,
            save_session_node=self.save_session_node,
        )

        self.restaurant_service = RestaurantService(db)
        self.booking_service = BookingService(db)

        self.registry.register(
            RestaurantInfoTool(
                self.restaurant_service
            )
        )
        self.registry.register(
            BookingTool(
                self.booking_service
            )
        )

        print("=" * 50)
        print("REGISTERED TOOLS")
        for tool in self.registry.list_tools():
            print(tool.name)
            print("=" * 50)
        self.graph = self.graph_builder.build()

    def run(
        self,
        customer_id: int,
        user_message: str,
    ) -> str:
        state = StateFactory.create(
            customer_id=customer_id,
            user_message=user_message,
        )

        result = self.graph.invoke(
            state,
            config={
                "configurable": {
                    "thread_id": str(customer_id)
                }
            }
        )

        return result["response"]
