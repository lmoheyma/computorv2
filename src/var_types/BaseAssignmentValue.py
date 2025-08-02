from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from environment.Environment import Environment

class BaseAssignmentValue(ABC):
    """Classe de base pour tous les types de valeurs assignables"""
    def __init__(self, name: str, value: Any, environment: 'Environment') -> None:
        self.name = name
        self.value = value
        self.environment = environment

    @abstractmethod
    def compute(self):
        pass

    @abstractmethod
    def __str__(self):
        pass