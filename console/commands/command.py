from abc import ABC, abstractmethod
from console.app_state import AppState
from functools import wraps

def requires_key(method: callable) -> callable:
    @wraps(method)
    def wrapper(self, state: AppState, args: list[str]) -> None:
        if state.api_key is None: 
            print("Error: API key not loaded")
            return
        return method(self, state, args)
    return wrapper

class Command(ABC):
    @abstractmethod
    def execute(self, state: AppState ,args: list[str]) -> None:
        ...