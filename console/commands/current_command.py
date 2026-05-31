from console.app_state import AppState
from .command import Command

class CurrentCommand(Command):
    """Prints the currently active Gemini model name."""

    def execute(self, state: AppState, args: list[str] = None) -> None:
        """
        Prints the name of the currently active Gemini model.

        Args:
            state: The shared AppState container.
            args: Optional command arguments (ignored).
        """
        print(f"Current active model: {state.current_model}")
