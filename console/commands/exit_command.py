from console.app_state import AppState
from .command import Command

class ExitCommand(Command):
    """Stops the session loop and exits the application."""
    def execute(self, state: AppState, args: list[str] = None) -> None:
        print("Exiting...")
        state.running = False