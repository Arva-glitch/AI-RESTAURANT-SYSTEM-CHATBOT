from sqlalchemy.orm import Session

from app.services.chatbot_session_service import (
    fetch_active_session,
    start_session,
    change_state,
    update_context
)


class SessionManager:

    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, customer_id: int):

        session = fetch_active_session(
            self.db,
            customer_id
        )

        if session:
            return session

        return start_session(
            self.db,
            customer_id
        )

    def set_state(
        self,
        session,
        state
    ):
        return change_state(
            self.db,
            session,
            state
        )

    def save_context(
        self,
        session,
        context
    ):
        return update_context(
            self.db,
            session,
            context
        )

    def get_state(self, session):
        return session.current_state

    def get_context(self, session):
        return session.context or {}

    def clear_context(self, session):
        return update_context(
            self.db,
            session,
            {}
        )
