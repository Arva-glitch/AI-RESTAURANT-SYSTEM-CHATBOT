from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from app.ai.graph.state import RestaurantState


class BaseTool(ABC):
    """
    Base class for every restaurant tool.
    """

    name: str
    description: str

    @abstractmethod
    def execute(
        self,
        state: RestaurantState,
    ) -> RestaurantState:
        """
        Execute the tool and update the graph state.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return self.name
