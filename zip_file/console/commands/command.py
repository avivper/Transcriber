"""
Abstract base and utilities for console commands.
"""

from abc import ABC, abstractmethod
from console.app_state import AppState
from functools import wraps

def requires_key(method: callable) -> callable:
    """
    Decorator that blocks execution and prints an error if the API key is not loaded.
    Used to protect commands that require Gemini API access.
    """
    @wraps(method)
    def wrapper(self, state: AppState, args: list[str]) -> None:
        if state.api_key is None: 
            print("Error: API key not loaded")
            return
        return method(self, state, args)
    return wrapper

class Command(ABC):
    """
    Abstract base class for all console commands.
    Enforces a consistent interface for the Session to execute operations.
    """

    @abstractmethod
    def execute(self, state: AppState ,args: list[str]=None) -> None:
        """
        Execute the command with the given application state and arguments.
        
        Args:
            state: The shared AppState container.
            args: Command-line arguments passed by the user.
        """
        ...
