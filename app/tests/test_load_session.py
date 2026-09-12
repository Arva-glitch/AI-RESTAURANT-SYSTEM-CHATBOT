from app.ai.graph.state_factory import StateFactory
from app.ai.graph.nodes.load_session_node import LoadSessionNode
from app.chatbot.session_manager import SessionManager
from app.database import SessionLocal  # Your DB session

db = SessionLocal()

session_manager = SessionManager(db)
load_session = LoadSessionNode(session_manager)

state = StateFactory.create(
    customer_id=1,
    user_message="Hi"
)

result = load_session(state)

print(result)

db.close()
